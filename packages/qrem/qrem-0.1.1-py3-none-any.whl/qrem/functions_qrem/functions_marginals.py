import copy
from typing import Dict
import multiprocessing

from tqdm import tqdm
import numpy as np

from qrem.functions_qrem import functions_data_analysis as fda, ancillary_functions as anf

from qrem.common.printer import qprint

#JT: Function used to compute marginals
#MOcomm: this function doubles functionalities of some of 
def compute_unnormalized_marginals_without_mp(
        multiple_experimental_results: Dict[str, Dict[str, int]],
        subsets_dictionary,
        print_progress_bar=False
):
    # print(subsets_list)

    #JT: check of the subset datatype. The procedure needs subsets as a list, so there is a coversion if they are provided as a dictionary

    if isinstance(subsets_dictionary,dict):

        #JT: dictionary entries encoding subsets are rewritten as subsets

        all_subsets = []
        for subsets_list_actual in subsets_dictionary.values():
            all_subsets = all_subsets+subsets_list_actual

    #JT: if subsets are given as a list it stays this way

    elif isinstance(subsets_dictionary,list):
        all_subsets = subsets_dictionary
    else:
        raise ValueError(f"Wrong datatype '{type(subsets_dictionary)}' for subsets")

    #JT: the varaiable below stors uniqe lenghts of qubit subsets

    unique_lengths = np.unique([len(x) for x in all_subsets])

    #JT: a nested dictionary
    #length -elements of unique_lengths list
    #index outcome - goes over all bit strings of lenght from unique_lengths list
    #index outcome is converted to a bitstring, if this is shorter than length it is filled with 0 to the left, this is key of the second dictionary
    #the value of the second dictionary is set to 0

    local_registers_dictionaries = {length:
                                        {anf.integer_to_bitstring(index_outcome,
                                                                  length):
                                             0.0
                                         for index_outcome in range(int(2 ** length))}
                                    for length in unique_lengths}


    items_iterable = multiple_experimental_results.items()

    if print_progress_bar:
        items_iterable = tqdm(items_iterable)

    marginals_dictionary = {}

    #JT: this for loop goes over experimental settings and results of experiments for a given setting

    for experiment_label, experimental_results in items_iterable:

        if isinstance(subsets_dictionary,dict):
            subsets_list = subsets_dictionary[experiment_label]
        else:
            subsets_list = subsets_dictionary
        #JT: copy creates a shallow copy of an object (changes in orginal object influece copy)

        vectors_dictionaries = {subset: copy.copy(local_registers_dictionaries[len(subset)]) for
                                subset in subsets_list}

        # vectors_list = [copy.copy(local_registers_dictionaries[len(subset)]) for
        #                         subset in subsets_list]
        # norm = 0


        # for outcome_bitstring, number_of_occurrences in experimental_results.items():
        #     for subset_index in range(len(subsets_list)):
        #         subset = subsets_list[subset_index]
        #
        #         tuple_now = ''.join([outcome_bitstring[qi] for qi in subset])
        #
        #         vectors_dictionaries[subset][tuple_now] += number_of_occurrences

        #JT: this is a loop over different subsets

        for subset_index in range(len(subsets_list)):

            #JT: consecutive subsets are chosen

            subset = subsets_list[subset_index]

            #JT: For a fixed experimental setting a loop over different

            for outcome_bitstring, number_of_occurrences in experimental_results.items():

                #JT: outcome bitstring for a given subset is established

                tuple_now = ''.join([outcome_bitstring[qi] for qi in subset])

                #JT: otcome statistics for this subset and outcome string are added

                vectors_dictionaries[subset][tuple_now] += number_of_occurrences

        # vectors_dictionaries = {subsets_list[subset_index]:vectors_list[subset_index]
        #                         for subset_index in range(len(subsets_list))}


            # norm += number_of_occurrences

       #JT the dictionary has a structure key: subset value, value an array with number of occurences
       #JT: I'm not sure, hoe the ordering of results id done, i.e. what is the relation between a place in array and the resulting bitstring
       #JT: I assume that 0 etry is all 0 result and so on, but this needs to be double-checked

        marginals_dict_for_this_experiment = {
            subset: np.array(list(vectors_dictionaries[subset].values())) for subset in
            subsets_list}
        marginals_dictionary[experiment_label] = marginals_dict_for_this_experiment

    return marginals_dictionary


#JT: A generall comment, multi-processing runs function over 
def compute_unnormalized_marginals_with_mp_over_experiments(
                                   multiple_experimental_results:Dict[str,Dict[str,int]],
                                   subsets_dictionary,
                                   number_of_threads=None
                                   ):

    if number_of_threads is None:
        number_of_threads = multiprocessing.cpu_count()-1

    experimental_keys = list(multiple_experimental_results.keys())
    number_of_experiments = len(experimental_keys)

    batch_size = -int(number_of_experiments//(-number_of_threads))

    arguments_list = []
    for thread_index in range(number_of_threads):
        slice_indices_now = slice(thread_index * batch_size,
                            (thread_index + 1) * batch_size)

        print_progress_bar = False

        keys_slice_now = experimental_keys[slice_indices_now]


        #that's the last pool thread with maximal number of function calls
        # (last thread has the least of them)
        if thread_index in[number_of_threads-2]:
            print_progress_bar=True

        dictionary_res_now = {key:multiple_experimental_results[key] for key in keys_slice_now}

        # print(subsets_dictionary.keys())
        if isinstance(subsets_dictionary,dict):
            arguments_list.append((dictionary_res_now,
                                   {key:subsets_dictionary[key] for key in keys_slice_now},
                                   print_progress_bar))
        elif isinstance(subsets_dictionary,list):
            arguments_list.append((dictionary_res_now,
                                   subsets_dictionary,
                                   print_progress_bar))
        else:
            raise ValueError(f"Wrong datatype '{type(subsets_dictionary)}' for subsets.")


    pool = multiprocessing.Pool(number_of_threads)
    results = pool.starmap_async(compute_unnormalized_marginals_without_mp,
                                 arguments_list
                                 )
    # qprint("Closing pool...")
    pool.close()
    qprint("\nJoining pool...")
    pool.join()
    qprint("\nGetting results from pool...")
    res_multiprocessing = results.get()


    # qprint("\nCombining results from threads...")
    all_results = {}

    for dictionary_thread in res_multiprocessing:
        all_results = {**all_results, **dictionary_thread}
    # qprint("Done, returning results.")

    return all_results

