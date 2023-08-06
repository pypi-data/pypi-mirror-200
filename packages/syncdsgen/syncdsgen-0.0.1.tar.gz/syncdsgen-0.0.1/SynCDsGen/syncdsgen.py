import torch
import pyro
import pandas as pd
import numpy as np
import re

def check_row_sum(tensor, tol=1e-6):
        row_sums = tensor.sum(dim=1)
        return torch.all(torch.abs(row_sums - 1) < tol)

class SyncCDsGeneratorConf:
    def __init__(self, bases=None, codons=None, start_codons=None,
                  stop_codons=None, AAs=None, translation_dict=None,
                  transition_prob_t=None, emission_prob_t=None, AAs_initial_prob_dist=None,
                  codon_length=None, constraints_dict=None):
        self.bases = bases
        self.codons = codons
        self.start_codons = start_codons
        self.stop_codons = stop_codons
        self.AAs = AAs
        self.translation_dict = translation_dict
        self.transition_prob_t = transition_prob_t
        self.emission_prob_t = emission_prob_t
        self.AAs_initial_prob_dist = AAs_initial_prob_dist
        self.codon_length = codon_length
        self.constraints_dict = constraints_dict

    def is_AA_start_AA(self, AA):
        coding_codons = self.translation_dict[AA]

        for codon in coding_codons:
            if codon in self.start_codons:
                return 1
        return 0

    def get_AAs_initial_prob_dist(self):
        start_codons_prob_dist = [self.is_AA_start_AA(AA) for AA in self.AAs]
        nb_start_AAs = start_codons_prob_dist.count(1)

        start_codons_prob_dist = np.array(start_codons_prob_dist)/ nb_start_AAs

        return(start_codons_prob_dist)


class SynCDsGenerator:
    def __init__(self, generatorConf:SyncCDsGeneratorConf):
        self.generatorConf = generatorConf
        self.AAs_indices_sequences = []
        self.CDs_indices_sequences = []

        #check the validity of the attributes of the generator configuration
        assert len(generatorConf.start_codons) > 0, "For yncCDsGeneratorConf, the list of start codons should not be empty" #the list of start codons should not be emtpy
        assert len(generatorConf.translation_dict) == len(generatorConf.AAs), "For yncCDsGeneratorConf, translation dict should have the same size with the AAs list" #the translation_dict and the AAs list should have the same size
        assert generatorConf.transition_prob_t.size()[0] == generatorConf.transition_prob_t.size()[1] == len(generatorConf.AAs), "The emission_prob_t should be a squared tensor, and its size should be equal to the size of the AAs list"

        max_nb_syn_codons = max([len(syn_codons) for syn_codons in self.generatorConf.translation_dict.values()])
        assert generatorConf.emission_prob_t.size()[1] == max_nb_syn_codons, f"The second dimension of the emission_prob_t tensor should be {max_nb_syn_codons}, got {generatorConf.emission_prob_t.size()[1]}"
        
        assert check_row_sum(self.generatorConf.emission_prob_t), "Each row of the emission_prob_t should sum up to 1"
        assert check_row_sum(self.generatorConf.transition_prob_t), "Each row of the transition_prob_t should sum up to 1"

        if self.generatorConf.codon_length is None:
            l = len(self.generatorConf.codons[0])
            assert all(len(codon) == l for codon in self.generatorConf.codons), f"All the codons should have the same length"
            self.generatorConf.codon_length = l
        else:
            assert all(len(codon) == self.generatorConf.codon_length for codon in self.generatorConf.codons), f"All the codons should have the same length, since the codon length had been set to {self.generatorConf.codon_length}"

    def AA_indices_sequence_to_AA_sequence(self, X):
        return ''.join([self.generatorConf.AAs[i] for i in X])

    def CD_indices_sequence_to_CD_sequence(self, X):
        """
            input:
                X: list of indices of the AAs of the sequence concate to the list of indices of the codons of the sequence
        """
        N = len(X)
        AA_ind,  CDs_ind = X[0:N//2], X[N//2:]

        return ''.join([self.generatorConf.translation_dict[self.generatorConf.AAs[a]][int(i)] for a, i in zip(AA_ind, CDs_ind)])
    
    def build_dataframe(self):
        AAs_sequences = np.apply_along_axis(self.AA_indices_sequence_to_AA_sequence, 1, self.AAs_indices_sequences)

        joined_sequences = np.hstack((self.AAs_indices_sequences, self.CDs__indices_sequences))
        CDs_sequences = np.apply_along_axis(self.CD_indices_sequence_to_CD_sequence, 1, joined_sequences)

        self.synthetic_data = pd.DataFrame({'AAs': AAs_sequences, 'CDs': CDs_sequences})


class StochasticSynCDsGenerator(SynCDsGenerator):
    def __init__(self, generatorConf:SyncCDsGeneratorConf):
        super().init__(generatorConf)

    def sample(self, n_samples=100, length=50):

        if self.generatorConf.AAs_initial_prob_dist is None:
            self.generatorConf.AAs_initial_prob_dist = self.generatorConf.get_AAs_initial_prob_dist()

        assert length > 3, f"Waiting length > 3, got {length}"

        AAs_samples = []
        CDs_samples = []

        for j in torch.arange(0, n_samples):
            hidden_states = []
            observations = []

            #generate the first AA of the AA sequence from the start codons
            state = pyro.sample("x_{}_0".format(j),
                                pyro.distributions.Categorical(torch.Tensor(self.generatorConf.AAs_initial_prob_dist)))
            emission_p_t = self.generatorConf.emission_prob_t[state]

            observation = pyro.sample("y_{}_0".format(j),
                                      pyro.distributions.Categorical(emission_p_t))
            
            hidden_states.append(state)
            observations.append(observation)

            for k in torch.arange(1, length-1):
                transition_p_t = self.generatorConf.transition_prob_t[state]
                state = pyro.sample("x_{}_{}".format(j, k),
                                    pyro.distributions.Categorical(transition_p_t))
                emission_p_t = self.generatorConf.emission_prob_t[state]

                observation = pyro.sample("y_{}_{}".format(j, k),
                                          pyro.distributions.Categorical(emission_p_t))

                hidden_states.append(state)
                observations.append(observation)   

            AA_sample = torch.Tensor(hidden_states)
            CDs_sample = torch.Tensor(observations)

            AAs_samples.append(AA_sample)
            CDs_samples.append(CDs_sample)

        self.AAs_indices_sequences = torch.vstack(AAs_samples).numpy().astype(int)
        self.CDs__indices_sequences = torch.vstack(CDs_samples).numpy().astype(int)

        self.build_dataframe()

        return self.synthetic_data


class AutoregressiveSynCDsGenerator(SynCDsGenerator):
    def __init__(self, generatorConf:SyncCDsGeneratorConf):
        SynCDsGenerator.__init__(self, generatorConf)

        assert len(self.generatorConf.constraints_dict) > 0, "For a StochasticSynCDsGenerator, we should set the SyncCDsGeneratorConf's constraints_dict to a non empty dictionary"

        assert all(AA in self.generatorConf.AAs for constraint in self.generatorConf.constraints_dict.values() for AA in constraint), "The AAs used in  SyncCDsGeneratorConf.constraints_dict should be present in SyncCDsGeneratorConf.AAs"

    def sample(self, n_samples=100, length=50):

        if self.generatorConf.AAs_initial_prob_dist is None:
            self.generatorConf.AAs_initial_prob_dist = self.generatorConf.get_AAs_initial_prob_dist()

        assert length > 3, f"Waiting length > 3, got {length}"

        AAs_samples = []
        CDs_samples = []

        for j in torch.arange(0, n_samples):
            hidden_states = []
            observations = []

            #generate the first AA of the AA sequence from the start codons
            state = pyro.sample("x_{}_0".format(j),
                                pyro.distributions.Categorical(torch.Tensor(self.generatorConf.AAs_initial_prob_dist)))
            emission_p_t = self.generatorConf.emission_prob_t[state]

            observation = pyro.sample("y_{}_0".format(j),
                                      pyro.distributions.Categorical(emission_p_t))
            
            hidden_states.append(state)
            observations.append(observation)

            for k in torch.arange(1, length-1):
                transition_p_t = self.generatorConf.transition_prob_t[state]
                state = pyro.sample("x_{}_{}".format(j, k),
                                    pyro.distributions.Categorical(transition_p_t))
                
                hidden_AAs_sequence = self.AA_indices_sequence_to_AA_sequence(hidden_states)

                emission_p_t = self.generatorConf.emission_prob_t[state]

                for pattern in self.generatorConf.constraints_dict:
                    constraints = self.generatorConf.constraints_dict[pattern]
                    if re.match(pattern, hidden_AAs_sequence) and self.generatorConf.AAs[state] in constraints:
                        emission_p_t = constraints[self.generatorConf.AAs[state]]
                        break

                observation = pyro.sample("y_{}_{}".format(j, k),
                                          pyro.distributions.Categorical(emission_p_t))

                hidden_states.append(state)
                observations.append(observation)   

            AA_sample = torch.Tensor(hidden_states)
            CDs_sample = torch.Tensor(observations)

            AAs_samples.append(AA_sample)
            CDs_samples.append(CDs_sample)

        self.AAs_indices_sequences = torch.vstack(AAs_samples).numpy().astype(int)
        self.CDs__indices_sequences = torch.vstack(CDs_samples).numpy().astype(int)

        self.build_dataframe()

        return self.synthetic_data
