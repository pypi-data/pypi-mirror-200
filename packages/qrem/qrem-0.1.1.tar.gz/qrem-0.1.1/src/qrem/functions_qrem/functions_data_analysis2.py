"""
@authors: Filip Maciejewski, Oskar Słowik, Tomek Rybotycki
@contact: filip.b.maciejewski@gmail.com
"""

from collections import defaultdict
from typing import Dict, List

import numpy as np
from qrem.functions_qrem import povmtools, ancillary_functions as anf
import copy


class KeyDependentDictForMarginals(defaultdict):
    """
    This is class used to store marginal probability distributions in dictionary.
    It is "key dependent" in the sense that if user tries to refer to non-existing value for some
    KEY, then this value is created as a marginal distribution which size depends on the KEY
    NOTE: We assume that provided KEY is a string denoting  qubits subset
    (see self.value_creating_function)


    COPYRIGHT NOTE
    The main idea of this code was taken from Reddit thread:
    https://www.reddit.com/r/Python/comments/27crqg/making_defaultdict_create_defaults_that_are_a/

    """

    def __init__(self):
        super().__init__(None)  # initialize as standard defaultdict

        # This is the function which takes the string "key" that is assumed to label qubits subset
        # in the form 'q2q3q11...' etc. It takes this key, calculates number of qubits N, and creates
        # empty vector of the size d=2^N.
        self.value_creating_function = lambda key: np.zeros(
            (int(2 ** len(anf.get_qubit_indices_from_keystring(key))), 1),
            dtype=float)

    # called when key is missing
    def __missing__(self, key):
        # calculate the key-dependent value
        ret = self.value_creating_function(key)
        # put the value inside the dictionary
        self[key] = ret
        return ret


class key_dependent_dict_for_marginals(defaultdict):
    """
    same as KeyDependentDictForMarginals but different name
    TODO FBM: refactor this
    """

    def __init__(self):
        super().__init__(None)  # initialize as standard defaultdict

        # This is the function which takes the string "key" that is assumed to label qubits subset
        # in the form 'q2q3q11...' etc. It takes this key, calculates number of qubits N, and creates
        # empty vector of the size d=2^N.
        self.value_creating_function = lambda key: np.zeros(
            (int(2 ** len(anf.get_qubit_indices_from_keystring(key))), 1),
            dtype=float)

    # called when key is missing
    def __missing__(self, key):
        # calculate the key-dependent value
        ret = self.value_creating_function(key)
        # put the value inside the dictionary
        self[key] = ret
        return ret


def get_state_from_circuit_name(circuit_name):
    state_name = ''
    for string in circuit_name:
        if string in ['1', 'X', 'x']:
            state_name += '1'
        elif string in ['0', 'I', 'i_index', 'id', 'Id']:
            state_name += '0'

    return state_name


def get_mini_dict(number_of_qubits):
    register = povmtools.register_names_qubits(range(number_of_qubits), number_of_qubits)
    return {key: np.zeros((int(2 ** number_of_qubits), 1)) for key in register}


def estimate_energy_from_marginals(weights_dictionary: Dict[str, float],
                                   marginals_dictionary: Dict[str, np.ndarray]):
    """
    Compute energy of Hamiltonian from dictionary of marginal distributions.

    :param weights_dictionary:
    :param marginals_dictionary:
    :return:
    """

    energy = 0
    for key_local_term in weights_dictionary.keys():
        weight = weights_dictionary[key_local_term]
        marginal = marginals_dictionary[key_local_term]

        qubits_number = int(np.log2(len(marginal)))

        for result_index in range(len(marginal)):
            bitstring = list(anf.integer_to_bitstring(result_index, qubits_number))
            bit_true = [int(x) for x in bitstring]
            parity = (-1) ** (np.count_nonzero(bit_true))
            energy += weight * marginal[result_index] * parity

    if isinstance(energy, list) or isinstance(energy, np.ndarray):
        return energy[0]
    else:
        return energy


import re


def get_energy_from_bitstring_diagonal(bitstring: str,
                                       weights_dict: Dict[str, float]
                                       ):
    energy = 0
    for qubits_string, hamiltonian_coefficient in weights_dict.items():
        qubit_indices = [int(q) for q in re.findall(r'\d+', qubits_string)]
        marginal_bitstring = [int(bitstring[q]) for q in qubit_indices]
        parity = (-1) ** (np.count_nonzero(marginal_bitstring))
        energy += parity * hamiltonian_coefficient

    return energy


def add_counts_from_dictionaries(counts_dictionaries_list: List[Dict[str, int]]) -> Dict[str, int]:
    """
    Merge multiple counts dictionaries.
    This is useful when you have results of multiple implementations of the same experiment.

    :param counts_dictionaries_list: list of results of counts dictionaries of the form:
                                    {'bitstring":number of measurements}
    :return:
    """

    # first dictionary will be template to which we will add counts
    merged_counts = copy.deepcopy(counts_dictionaries_list[0])

    # we go through all other dictionaries
    for counts_dictionary in counts_dictionaries_list[1:]:
        for bitstring, ticks in counts_dictionary.items():
            if bitstring in merged_counts.keys():
                merged_counts[bitstring] += ticks
            else:
                merged_counts[bitstring] = ticks

    return merged_counts


def convert_counts_overlapping_tomography(counts_dictionary: Dict[str, Dict[str, int]],
                                          experiment_name: str):
    def string_cutter(circuit_name: str):
        """
        This function cuts the name of the circuit to the format that will later be used by
        tomography data analyzers.


        :param circuit_name:
        It assumes the following convention:

        circuit_name = "experiment name" + "-" + "circuit label"+
        "no"+ "integer identifier for multiple implementations of the same circuit"

        for example the circuit can have name:
        "DDOT-010no3"

        which means that this experiment is Diagonal Detector Overlapping Tomography (DDOT),
        the circuit implements state "010" (i.e., gates iden, X, iden on qubits 0,1,2), and
        in the whole circuits sets this is the 4th (we start counting from 0) circuit that implements
        that particular state.

        :return:
        """
        experiment_string_len = len(list(experiment_name))
        full_name_now = circuit_name[experiment_string_len + 1:]
        new_string = ''
        for symbol_index in range(len(full_name_now)):
            if full_name_now[symbol_index] + full_name_now[symbol_index + 1] == 'no':
                break
            new_string += full_name_now[symbol_index]
        return new_string

    big_counts_dictionary = {}

    for circuit_name, counts_dict_now in counts_dictionary.items():
        proper_name_now = string_cutter(circuit_name)
        if proper_name_now not in big_counts_dictionary.keys():
            big_counts_dictionary[proper_name_now] = counts_dict_now
        else:
            big_counts_dictionary[proper_name_now] = add_counts_from_dictionaries(
                [big_counts_dictionary[proper_name_now], counts_dict_now])

    return big_counts_dictionary


import scipy as sc
def get_CTMP_rates_from_results(results_dictionary_ddot: Dict[str, Dict[str, int]],
                                number_of_qubits: int):
    single_qubits = list(range(number_of_qubits))
    pairs = [(i, j) for i in range(number_of_qubits) for j in range(i + 1, number_of_qubits)]

    local_noise_matrices_CTMP = {pair: np.zeros((4, 4), dtype=float) for pair in pairs}

    for pair in pairs:
        pair_complement = list(set(single_qubits).difference(set(pair)))

        for global_input_state, results_dictionary in results_dictionary_ddot.items():
            marginal_input_state = ''.join([global_input_state[x] for x in pair])
            input_state_complement = [global_input_state[x] for x in pair_complement]

            for global_output_state, ticks in results_dictionary.items():
                marginal_output_state = ''.join([global_output_state[x] for x in pair])
                output_state_complement = [global_output_state[x] for x in pair_complement]

                if output_state_complement == input_state_complement:
                    # check if this is their convention!
                    local_noise_matrices_CTMP[pair][int(marginal_output_state, 2),
                                               int(marginal_input_state, 2)] += ticks

    # normalize to stochastic matrices
    for pair in pairs:
        for k in range(4):
            local_noise_matrices_CTMP[pair][:, k] /= sum(local_noise_matrices_CTMP[pair][:, k])

    # Get G matrices
    G_matrices = {pair: sc.linalg.logm(local_noise_matrices_CTMP[pair]) for pair in pairs}

    # ancillary function
    def _chop_negatives(M):
        (m, n) = M.shape

        chopped_M = copy.deepcopy(M)
        for i in range(m):
            for j in range(n):
                if i != j and M[i, j] < 0:
                    chopped_M[i, j] = 0

        return chopped_M

    # Get G' matrices
    G_prime_matrices = {pair: _chop_negatives(G_matrices[pair]) for pair in pairs}

    rates_dictionary_1q = {f"q{q}": {'0': 0, '1': 0} for q in single_qubits}
    for qj in single_qubits:
        r0, r1 = 0, 0

        for q_other in single_qubits:
            if q_other != qj:
                G_prime_matrix_now = G_prime_matrices[tuple(sorted([qj, q_other]))]

                r0 += G_prime_matrix_now[2, 0] + G_prime_matrix_now[3, 1] \
                    # +G_prime_matrix_now[1,0]+G_prime_matrix_now[3,2]

                r1 += G_prime_matrix_now[0, 2] + G_prime_matrix_now[1, 3] \
                    # +G_prime_matrix_now[0, 1] + G_prime_matrix_now[2, 3]

        r0 /= 2 * (number_of_qubits - 1)
        r1 /= 2 * (number_of_qubits - 1)

        rates_dictionary_1q[f"q{qj}"]['0'] = r0
        rates_dictionary_1q[f"q{qj}"]['0'] = r1

    rates_dictionary_2q = {f"q{pair[0]}q{pair[1]}": {'00': 0,
                                                     '01': 0,
                                                     '10': 0,
                                                     '11': 0} for pair in pairs}

    for pair in pairs:
        G_prime_matrix_now = G_prime_matrices[pair]
        rates_dictionary_2q[f"q{pair[0]}q{pair[1]}"]['00'] = G_prime_matrix_now[3, 0]
        rates_dictionary_2q[f"q{pair[0]}q{pair[1]}"]['01'] = G_prime_matrix_now[2, 1]
        rates_dictionary_2q[f"q{pair[0]}q{pair[1]}"]['10'] = G_prime_matrix_now[1, 2]
        rates_dictionary_2q[f"q{pair[0]}q{pair[1]}"]['11'] = G_prime_matrix_now[0, 3]

    rates_dictionary = {**rates_dictionary_1q,
                        **rates_dictionary_2q}

    return rates_dictionary

def convert_counts_dictionary_to_probability_distribution(counts_dictionary):
    number_of_qubits = len(list(list(counts_dictionary.keys())[0]))
    probability_distribution = np.zeros((2 ** number_of_qubits), dtype=float)
    normalization_shots = sum(list(counts_dictionary.values()))

    for key, shots in counts_dictionary.items():
        probability_distribution[int(key, 2)] += shots / normalization_shots
    return probability_distribution