from typing import List, Dict, Union, Optional

import numpy as np
from tqdm import tqdm

from functions_qrem import povmtools
from functions_qrem.povmtools import reorder_probabilities
from qrem.data_structures.datastructure_base import DataStructureBase


# ORGANIZE: this needs exception handling and securing against bad data
# ORGANIZE: write setters for all attributes or converter modules will handle this?
# ORGANIZE: the functions for converting between formats are copied from qiskit_utilities
# TEST: all of this.
class ExperimentResults(DataStructureBase):
    """
    The class contains data about results of an experiment.
    Parameters
    ----------
    frequencies_array (np.array(c, 2^q)): array, where c is # of circuits, q is # of qubits, each entry contains
            frequency of a given state occurring in experiment result for given circuit.
            Possible states in a row are numbered increasingly from |00000 ... 0>, |10000 ... 0> up to |1111 ... 1>,
            qubit and classical outcome ordering - big endian: 0123...
            Example: [[0.25, 0.00, 0.30, 0.45],
                      [0.00, 0.50, 0.50, 0.00]] is a result of 2 circuits on 2 qubits,
                      where in the first circuit outcome |00> occurred in 25% of shots, |10> in 0%, |01> in 0.30 etc.#TODO check if this is how we've used it so far

    counts (dict): the key is the name of a circuit (str), the value is a dictionary of counts, where the key is a
            string denoting classical outcome and the value the number of its occurrences in given experiment.
            The circuits are named according to convention:
            circuit_name = "experiment name" + "-" + "circuit label" +
            "no" + "integer identifier for multiple implementations of the same circuit", e.g.: "DDOT-010no3"
    probabilities_list (List):
    tasks_IDs (str): device-specific ID for each circuit in the experiment, ordered #TODO - order how?
    datetime_obtained_utc: date of obtaining experiment results

    """

    def __init__(self):
        super().__init__()
        self.frequencies_array = None
        self.counts = None
        self.tasks_IDs = None
        self.notes = ''
        self.datetime_obtained_utc = None

    def __init__(self, frequencies_array):
        self.__init__()
        self.frequencies_array = frequencies_array

    def __init__(self, counts):
        self.__init__()
        self.counts = counts

    def load_from_dict(self, dictionary):
        for key in dictionary:
            if key in self.get_dict_format():
                setattr(self, key,
                        dictionary[key])  # TODO: secure against bad data
        pass

    def get_counts_from_frequencies_array(self):
        if self.frequencies_array is None:
            raise Exception("Frequencies array is empty")
        else:
            pass

    # ORGANIZE: The three methods below are copied functions from qiskit_utilities. Refactor
    def get_frequencies_array_from_probabilities_list(self, frequencies_list: List[Union[List[float], np.ndarray]],
                                                      reverse_order: Optional[bool] = False):
        """
        :param frequencies_list: list of probabilities estimated in experiments
        :param reverse_order: specify whether probabiltiies lists should be reordered, which corresponds
                              to changing qubits' ordering

        """

        number_of_qubits = int(np.log2(len(frequencies_list[0])))
        frequencies_formatted = frequencies_list
        if reverse_order:
            frequencies_formatted = [reorder_probabilities(probs, range(number_of_qubits)[::-1])
                                     for probs in frequencies_list]

        frequencies_array = np.ndarray(shape=(len(frequencies_list), len(frequencies_list[0])))

        for probe_state_index in range(len(frequencies_list)):
            frequencies_array[probe_state_index][:] = frequencies_formatted[:]
        return frequencies_array


    def get_frequencies_from_counts(counts_dict,
                                    crs=None,
                                    classical_register=None,
                                    shots_number=None,
                                    reorder_bits=True):
        if crs is None:
            crs = len(list(list(counts_dict.keys())[0]))

        d = 2 ** crs

        if classical_register is None:
            classical_register = ["{0:b}".format(i).zfill(crs) for i in range(d)]

        normal_order = []

        for j in range(d):
            if classical_register[j] in counts_dict.keys():
                counts_now = counts_dict[classical_register[j]]
                normal_order.append(counts_now)

            else:
                normal_order.append(0)
        if reorder_bits:
            frequencies = reorder_probabilities(normal_order, range(crs)[::-1])
        else:
            frequencies = normal_order

        if shots_number is None:
            frequencies = frequencies / np.sum(frequencies)
        else:
            frequencies = frequencies / shots_number

        return frequencies

    def add_counts_dicts(all_counts, modulo, dimension):
        frequencies = [np.zeros(dimension) for i in range(modulo)]

        for counts_index in tqdm(range(len(all_counts))):
            true_index = counts_index % modulo

            freqs_now = povmtools.counts_dict_to_frequencies_vector(all_counts[counts_index], True)
            frequencies[true_index][:] += freqs_now[:]

            # print(freqs_now)
        for i in range(modulo):
            frequencies[i] *= 1 / np.sum(frequencies[i])

        return frequencies
