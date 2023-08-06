import copy
import time
from typing import Optional, Dict, List, Tuple
import multiprocessing as mp

import numpy as np

from qrem.functions_qrem import functions_data_analysis as fda
from qrem.functions_qrem import functions_marginals as funmarg
from qrem.noise_characterization.base_classes.marginals_analyzer_interface import MarginalsAnalyzerInterface

# from qrem.common.printer import qprint


class MarginalsAnalyzerBase(MarginalsAnalyzerInterface):
    """
    This is base class for all the classes that will operate on marginal probability distributions.
    Methods of this class allow to calculate marginal distributions from experimental results.

    In this class and its children, we use the following convention for:

     1. Generic experimental results:
    :param results_dictionary: Nested dictionary with following structure:

    results_dictionary[label_of_experiment][bitstring_outcome] = number_of_occurrences

    where:
        -label_of_experiment is arbitrary label for particular experiment,
        -bitstring_outcome is label for measurement outcome,
        -number_of_occurrences is number of times that bitstring_outcome was recorded

        Hence top-level key labels particular experiment
        (one can think about quantum circuit implementation)
        and its value is another dictionary with results of given experiment in the form
        of dictionary of measurement outcomes


    2. Results represented as marginal probability distributions:
        :param marginals_dictionary: Nested dictionary with the following structure:

        marginals_dictionary[label_of_experiment][label_of_subset] = marginal_probability_vector

        where:
            -label_of_experiment is the same as in results_dictionary and it labels results from which
            marginal distributions were calculated
            -label_of_subset is a label for qubits subset for which marginals_dictionary were calculated.
            We use convention that such label label is tuple of integers indicating qubits' indices
            -marginal_probability_vector marginal distribution stored as vector

    """

    # TODO FBM: add coarse-graining functions_qrem for marginals_dictionary as class methods

    def __init__(self,
                 results_dictionary: Dict[str, Dict[str, int]],
                 bitstrings_right_to_left: Optional[bool]=False,
                 marginals_dictionary: Optional[Dict[str, Dict[Tuple[int], np.ndarray]]] = None,
                 ) -> None:

        """
        :param results_dictionary: see class description

        :param bitstrings_right_to_left: specify whether bitstrings
                                    should be read from right to left (when interpreting qubit labels)
        :param marginals_dictionary: see class description

        NOTE: when user does not provide marginals_dictionary we create it during class initialization.
        To this aim, we create "key_dependent_dicts" (see below)
        """

        if marginals_dictionary is None:
            # If user does not provide dictionary with marginals_dictionary, we create template.
            # Instead of standard dictionaries, we use ones that are "key dependent" (see description
            # of that function), which is useful for some calculations. This is because it allows to
            # not care whether given probability distribution was already created (as value in
            # dictionary) - if not, it creates it on the run.
            marginals_dictionary_key_dependent = {key: {}
                                                  for key in results_dictionary.keys()}
        else:
            marginals_dictionary_key_dependent = {}
            # print(marginals_dictionary)
            for experiment_key, local_dict in marginals_dictionary.items():

                if isinstance(local_dict, dict):
                    new_dict = {}
                    for key, value in local_dict.items():
                        new_dict[key] = value
                else:
                    new_dict = local_dict
                marginals_dictionary_key_dependent[experiment_key] = new_dict

        # print(list(results_dictionary.values())[0])
        # raise KeyError

        # set initial values of class properties
        self._results_dictionary = results_dictionary
        self._marginals_dictionary = marginals_dictionary_key_dependent
        self._bitstrings_right_to_left = bitstrings_right_to_left


        first_experiment = list(results_dictionary.values())[0]
        # print(first_experiment)
        try:
            self._number_of_qubits = len(list(first_experiment.keys())[0])
        except(AttributeError):
        #     print(results_dictionary)
            print(type(first_experiment))
        #
            raise KeyboardInterrupt


        # print(self._number_of_qubits)
        self._qubit_indices = list(range(self._number_of_qubits ))



    @property
    def results_dictionary(self) -> Dict[str, Dict[str, int]]:

        return self._results_dictionary

    @results_dictionary.setter
    def results_dictionary(self, results_dictionary: Dict[str, Dict[str, int]]) -> None:
        self._results_dictionary = results_dictionary

    @property
    def marginals_dictionary(self) -> Dict[str, Dict[Tuple[int], np.ndarray]]:

        # if np.any([str(type(dictionary))!="<class 'dict'>" for dictionary in self._marginals_dictionary.values()]):
        #     dict_to_return = {}
        #     for experiment_key, key_dependent_dict in self._marginals_dictionary.items():
        #         dict_to_return[experiment_key] = dict(key_dependent_dict)
        # else:
        #     dict_to_return = self._marginals_dictionary
        #
        #
        # if str(type(dict_to_return))!="<class 'dict'>":
        #     dict_to_return = dict(dict_to_return)
        #
        #
        # self._marginals_dictionary = dict_to_return


        return self._marginals_dictionary

    @marginals_dictionary.setter
    def marginals_dictionary(self,
                             marginals_dictionary: Dict[str, Dict[Tuple[int], np.ndarray]]) -> None:
        self._marginals_dictionary = marginals_dictionary


    def results_dictionary_update(self,
                                  results_dictionary_new: Dict[str, Dict[str, int]]) -> None:
        # This method_name updates results dictionary from class property with new dictionary.
        # Note that if there is KEY collision, then the value from new dictionary overwrites old one.

        self._results_dictionary = {**self._results_dictionary,
                                    **results_dictionary_new}

    def marginals_dictionary_update(self,
                                    marginals_dictionary_new: Dict[
                                        str, Dict[Tuple[int], np.ndarray]]) -> None:
        # See description of self.results_dictionary_update

        self._marginals_dictionary = {**self._marginals_dictionary,
                                      **marginals_dictionary_new}


    # @staticmethod
    # def normalize_marginals(results):
    #
    #     for key_experiment in results.keys():
    #





    def normalize_marginals(self,
                            experiments_keys: Optional[List[str]] = None,
                            marginals_keys: Optional[Dict[str,Tuple[int]]] = None) -> None:
        """Go through marginals_dictionary stored as class' property
           and normalize marginal distributions
        :param experiments_keys: labels for experiments
        :param marginals_keys: labels for qubit subsets_list
        """
        # If no labels of experiments are provided, we take all of them
        if experiments_keys is None:
            experiments_keys = self._marginals_dictionary.keys()

        # Loop through all experiments and marginals_dictionary and normalize them.
        for key_experiment in experiments_keys:
            if marginals_keys is None:
                # if no marginal keys are provided, we take all of them
                looping_over = self._marginals_dictionary[key_experiment].keys()
            else:
                looping_over = marginals_keys[key_experiment]

            for key_marginal in looping_over:
                self._marginals_dictionary[key_experiment][key_marginal] *= 1 / np.sum(
                    self._marginals_dictionary[key_experiment][key_marginal])

#JT this is method is used to compute marginals
    @staticmethod
    def __compute_unnormalized_marginals_without_mp(
                                       multiple_experimental_results:Dict[str,Dict[str,int]],
                                       subsets_list:List[List[int]]
                                       ):

        #JT: it uses function_marginals from functions qrem
        return funmarg.compute_unnormalized_marginals_without_mp(multiple_experimental_results=multiple_experimental_results,
                                                                 subsets_dictionary=subsets_list)

    @staticmethod
    def __compute_unnormalized_marginals_with_mp(
                                       multiple_experimental_results:Dict[str,Dict[str,int]],
                                       subsets_dictionary,
            number_of_threads=None
                                       ):





        return funmarg.compute_unnormalized_marginals_with_mp_over_experiments(multiple_experimental_results=multiple_experimental_results,
                                                                               subsets_dictionary=subsets_dictionary,
                                                                               number_of_threads=number_of_threads)


    #JT: this function is used to compute marginals for a fixed setting of tomography experiment

    def compute_unnormalized_marginals(self,
                                       experiment_keys: List[str],
                                       subsets_dictionary: List[Tuple[int]],
                                       # normalize_marginals=False,
                                       multiprocessing=True) -> None:
        """Return dictionary of marginal probability distributions from counts dictionary
        :param experiment_keys: list of keys that label experiments for which marginals_dictionary should be taken
        :param subsets_dictionary: list of subsets_list of qubits for which marginals_dictionary should be calculated
        """

        #TODO FBM: update class property

        if isinstance(experiment_keys,str):
            experiment_keys = [experiment_keys]

        #JT: This is used for multiprocessing

        if multiprocessing:
            marginals_dictionary = self.__compute_unnormalized_marginals_with_mp(multiple_experimental_results={key:self._results_dictionary[key] for key in experiment_keys},
                                                                                 subsets_dictionary=subsets_dictionary)
        #JT: this is used if multiprocessing is not chosen

        else:
            marginals_dictionary = self.__compute_unnormalized_marginals_without_mp(multiple_experimental_results={key:self._results_dictionary[key] for key in experiment_keys},
                                                                                    subsets_list=subsets_dictionary)

        return marginals_dictionary




        # self.normalize_marginals(experiments_keys=experiment_keys,
        #                          marginals_keys=subsets_list)

                    # return marginals_dict_test_big


    def compute_marginals_old(self,
                          experiment_keys: List[str],
                          subsets_list: List[Tuple[int]]) -> None:
        """Return dictionary of marginal probability distributions from counts dictionary
        :param experiment_keys: list of keys that label experiments for which marginals_dictionary should be taken
        :param subsets_list: list of subsets_list of qubits for which marginals_dictionary should be calculated
        """

        if isinstance(experiment_keys, str):
            experiment_keys = [experiment_keys]

        # new_subsets_to_normalize = []
        for experiment_label in experiment_keys:
            experimental_results = self._results_dictionary[experiment_label]

            for subset in subsets_list:
                # if tuple(subset) in self._marginals_dictionary[experiment_label].keys():
                #     continue
                # else:
                # new_subsets_to_normalize.append(tuple(subset))

                # initialize marginal distribution
                marginal_vector_now = np.zeros((int(2 ** len(subset)), 1),
                                               dtype=float)
                for outcome_bitstring, number_of_occurrences in experimental_results.items():
                    if self._bitstrings_right_to_left:
                        # here we change the order of bitstring if it was specified
                        outcome_bitstring = outcome_bitstring[::-1]

                    # get bitstring denoting state of qubits in the subset
                    marginal_key_now = ''.join([outcome_bitstring[b] for b in subset])

                    # add counts to the marginal distribution
                    marginal_vector_now[int(marginal_key_now, 2)] += number_of_occurrences

                # Here if there is no "qubits_string" KEY we use the fact that by default we use
                # "key_dependent_dictionary". See description of __init__.
                self._marginals_dictionary[experiment_label][tuple(subset)] += marginal_vector_now
                # print(marginal_vector_now, marginal_vector_now/np.sum(marginal_vector_now))

        # self.normalize_marginals(experiment_keys, new_subsets_to_normalize)


    #JT: this is the method to compute marginals
    #MOcomm - name of this method is a bit wierd - I suggest changing it
    def compute_all_marginals(self,
                              subsets_dictionary: List[Tuple[int]],
                              multiprocessing=False,
                              check_if_already_calculated=False,
                              show_progress_bar = True) -> None:

        """
        #TODO FBM: add multiprocessing for this task
        #TODO FBM: change subsets_list to be dictionary
        Implements self.compute_marginals for all experimental keys.

        :param subsets_dictionary: list of subsets of qubits for which marginals_dictionary should be calculated
        :param show_progress_bar: if True, shows progress bar. Requires "tqdm" package
        """


        t0 = time.time()

        #JT: key list is a list of different experiment settings

        keys_list = list(self._results_dictionary.keys())
        keys_list_range = range(len(keys_list))

        # if progress bar should be shown, we use tqdm package
        if show_progress_bar:
            from tqdm import tqdm
            keys_list_range = tqdm(keys_list_range)

        #JT: subsets_dictionary -  A dictionary with keys -experimental settings and values - lists of subsets

        if isinstance(subsets_dictionary, list):



            subsets_dict = {key:subsets_dictionary for key in keys_list}
            subsets_dictionary = subsets_dict

        # print('\nsubsets input:', subsets_list)
        # print('\nsubsets existing:',self._marginals_dictionary)

        subsets_to_compute = {key:[] for key in keys_list}

        #JT: Loop below checks wheter some of the marginals have been computed previously

        if check_if_already_calculated:

            keys_outer_computed = self._marginals_dictionary.keys()
            for key in keys_list:

                if key not in keys_outer_computed:
                    subsets_to_compute[key] = subsets_dictionary[key]
                    # print(key)
                    # raise KeyboardInterrupt("WTF")
                else:
                    keys_inner_computed = self._marginals_dictionary[key].keys()
                    # for subset in subsets_dictionary:
                    #     if subset not in keys_inner_computed:
                    #         subsets_to_compute[key].append(subset)
                    subsets_to_compute[key] = [subset
                                              for subset in subsets_dictionary[key]
                                              if subset not in
                                              keys_inner_computed]
                    # print('hej2')
                    # print(keys_inner_computed)

        else:
            subsets_to_compute = {key:subsets_dictionary[key] for key in keys_list}

        #
        # print('\nsubsets to compute:', subsets_to_compute)
        # raise KeyboardInterrupt

        if not multiprocessing:
            big_marginals_dict = {}

            #This is a loop that goes over consecutive settings of tomographic experiments

            for key_index in keys_list_range:
                key = keys_list[key_index]

               #mrginals computation for a fixed setting is performed

                big_marginals_dict[key] = self.compute_unnormalized_marginals([key],
                                                                              {key:subsets_to_compute[key]},
                                                                              multiprocessing=False)[key]

        else:

            big_marginals_dict = self.compute_unnormalized_marginals(experiment_keys=keys_list,
                                                                     subsets_dictionary=subsets_to_compute,
                                                                     multiprocessing=True)
        # print(big_marginals_dict)
        # raise KeyboardInterrupt
        t1=time.time()
        for experiment_key, marg_dict in big_marginals_dict.items():

            # print(marg_dict)
            if experiment_key not in self._marginals_dictionary.keys():
                self._marginals_dictionary[experiment_key] = {}

            for subset, marginals_dictionary_local in marg_dict.items():

                # if subset not in self._marginals_dictionary[experiment_key].keys():
                # TODO FBM: perhaps consider addition instead of replacement
                self._marginals_dictionary[experiment_key][subset] = marginals_dictionary_local
                # else:
                #
                #     print(subset, marginals_dictionary_local)
                #     self._marginals_dictionary[experiment_key][subset] = {**self._marginals_dictionary[experiment_key][subset],
                #                                                           **marginals_dictionary_local}


        t2 = time.time()

        self.normalize_marginals(experiments_keys=keys_list,
                                 marginals_keys=subsets_to_compute)

        t3=time.time()
        #
        # qprint("\nCalculating marginals took:",t1-t0)
        # qprint("Updating dictionary in class took:",t2-t1)
        # qprint("Normalizing marginals took:",t3-t2)
        #
        #




    def get_marginals(self,
                      experiment_key: str,
                      subsets_list: List[Tuple[int]]) -> Dict[Tuple[int], np.ndarray]:
        """Like self.compute_marginals but first checks if the marginals_dictionary are already computed
            and it returns them.

        :param experiment_key: key that labels experiment from which marginals_dictionary should be taken
        :param subsets_list: list of subsets_list of qubits for which marginals_dictionary should be calculated

        :return: marginals_dictionary:
                dictionary in which KEY is label for subset, and VALUE is marginal on that subset
        """


        for subset in subsets_list:
            if experiment_key not in self._marginals_dictionary.keys():
                self.compute_unnormalized_marginals([experiment_key], [subset])
            elif subset not in self._marginals_dictionary[experiment_key].keys():
                self.compute_unnormalized_marginals([experiment_key], [subset])

        return {subset: self._marginals_dictionary[experiment_key][subset]
                for subset in subsets_list}

    @staticmethod
    def get_marginal_from_probability_distribution(
            global_probability_distribution: np.ndarray,
            bits_of_interest: List[int],
            register_names: Optional[List[str]] = None) -> np.ndarray:

        """Return marginal distribution from vector of global distribution
        :param global_probability_distribution: distribution on all bits
        :param bits_of_interest: bits we are interested in (so we average over other bits)
                                Assuming that qubits are labeled
                                from 0 to log2(len(global_probability_distribution))
        :param register_names: bitstrings register, default is
                               '00...00', '000...01', '000...10', ..., etc.

        :return: marginal_distribution : marginal probability distribution

        NOTE: we identify bits with qubits in the variables bitstring_names
        """

        return fda.get_marginal_from_probability_distribution(global_probability_distribution=global_probability_distribution,
                                                              bits_of_interest=bits_of_interest,
                                                              register_names=register_names)

    #JT: In this method an error occures when subset dictionary is restricted to some set of settings

    def compute_average_marginal_for_subset(self,
                                            subset):

        marginals_dictionary = self._marginals_dictionary

        marginal_dict_now = {}
        subset = tuple(subset)

        for input_state_bitstring, dictionary_marginals_now in marginals_dictionary.items():
            #JT: a marginal is constructed out of qubits belonging to subset
            input_marginal = ''.join([input_state_bitstring[x] for x in subset])
            #JT: computations of the marginal is perfored
            if subset not in dictionary_marginals_now.keys():
                self.compute_unnormalized_marginals([input_state_bitstring], [subset])

            if input_marginal not in marginal_dict_now.keys():
                marginal_dict_now[input_marginal] = dictionary_marginals_now[subset]
            else:
                marginal_dict_now[input_marginal] += dictionary_marginals_now[subset]

        for key_small in marginal_dict_now.keys():
            marginal_dict_now[key_small] /= np.sum(marginal_dict_now[key_small])

        return marginal_dict_now

    def get_averaged_marginal_for_subset(self,
                                         subset: Tuple[int]):

        #TODO FBM: I think it does not work here, different format
        marginals_dictionary = self._marginals_dictionary

        if subset in marginals_dictionary.keys():
            return marginals_dictionary[subset]
        else:
            return self.compute_average_marginal_for_subset(subset)

        # subset_key = 'q' + 'q'.join([str(s) for s in subset])
