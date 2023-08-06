
#ORGANIZE - would be great to know what is the role of all these packages
#--------------------------------------------------
# standard and technical imports 
#--------------------------------------------------
import os
import warnings
import re
import itertools #ORGANIZE - would be good if we trie dto be effitienta and used fast structures for iterations. @Piotr: this should be fast
import multiprocessing
import datetime as dt 
from collections import defaultdict
from typing import List, Dict, Optional, Callable, Tuple
import pickle
 
#--------------------------------------------------
# scientific imports
#--------------------------------------------------
import cmath as c
import numpy as np
import pandas as pd
from colorama import Fore, Style

from qrem.common.printer import qprint
#--------------------------------------------------
# local imports
#--------------------------------------------------
#NONE

# =======================================================================================
# FUNCTIONS TO BE MOVED TO core.utils, make new class Bitstring
# =======================================================================================

#MOVE_TO >> core.utils.DitConverter 
# ORGANIZE this function appears only here and probably can be deleted (MO)
def bitstring_to_integer(bitstring: str) -> int:
    return int(bitstring, 2)

#MOVE_TO >> core.utils.DitConverter
#TODO use numpy (bin(j)[2:])
#MOcomm function bellow is well documented and tested
def integer_to_bitstring(integer: int,
                         number_of_bits: int) -> str:
    """
    Return binary representation of an integer in a string form
    :param integer: input integer
    :param number_of_bits:
    NOTE: number of bits can be greater than minimal needed to represent integer (but if the input number of bits
     is smaller then the minimal one, the latter one will be executed )
    """
    return "{0:b}".format(integer).zfill(number_of_bits)

#MOVE_TO >> core.utils.DitConverter
def negate_bitstring(bitstring):
    '''
    this function creates a negation of a bitstring (assuming it is in string format)
    '''
    return ''.join('1' if x == '0' else '0' for x in bitstring)
    # potentially better version? Is it really useful?
    # def negate_bitstring(bit):
    #     if isinstance(bit,int) or isinstance(bit,float) or isinstance(bit,complex):
    #         if bit==0:
    #             return 1
    #         elif bit==1:
    #             return 0
    #         else:
    #             raise ValueError(f"Wrong bit: {bit}")
    #     elif isinstance(bit,str):
    #         if bit in ['0']:
    #             return '1'
    #         elif bit in ['1']:
    #             return '0'
    #         else:
    #             raise ValueError(f"Wrong bit: {bit}")
    #     else:
    #         raise ValueError(f"Wrong datatype of {bit} - '{type(bit)}'")
    pass

#MOVE_TO >> core.utils.DitConverter
def integer_to_ditstring(integer, base, number_of_dits):
    """

    based on
    https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base

    """
    if integer == 0:
        return [0 for _ in range(number_of_dits)]
    digits = []
    while integer:
        digits.append(int(integer % base))
        integer //= base

    # digits = sorted(digits,key = lambda x: x[0])
    # print(digits, digits[0])
    if len(digits) < number_of_dits:
        # print(len(digits),number_of_dits)
        for _ in range(number_of_dits - len(digits)):
            digits.append(0)
    # print(digits)

    return digits[::-1]
    
#MOVE_TO >> core.utils core.numerics
def get_ditstrings_register(base, number_of_dits):
    """ list of natural numbers fitting in number_of_dits with base dit-representation """
    return [integer_to_ditstring(j, base, number_of_dits=number_of_dits) for j in
            list(range(base ** number_of_dits))]

#MOVE_TO >> core.utils 
def integer_to_charstring(integer: int):
    if integer < 10:
        return str(integer)
    else:
        return chr(integer + 97 - 10)

#MOVE_TO >> core.utils
def get_qubit_indices_from_keystring(qubits_string: str,
                                  with_q: Optional[bool] = False) -> List[int]:
    """Return list of qubit indices from the string of the form "q0q1q22q31"
    :param qubits_string (string): string which has the form of "q" followed by qubit index
    :param (optional) with_q (Boolean): specify whether returned indices
                                        should be in form of string with letter

    :return: list of qubit indices:

    depending on value of parameter "with_q" the mapping will be one of the following:

    if with_q:
        'q1q5q13' -> ['q1','q5','q13']
    else:
        'q1q5q13' -> [1,5,13]
    """

    numbers = re.findall(r'\d+', qubits_string)

    if with_q:
        qubits = ['q' + s for s in numbers]
    else:
        qubits = [int(s) for s in numbers]

    return qubits

#MOVE_TO >> core.utils
# core.utils.DitstringConverter
# MO - check if usage makes sense? Can be iefficient
def get_qubits_keystring(list_of_qubits: List[int]) -> str:
    """ from subset of qubit indices get the string that labels this subset
        using convention 'q5q6q12...' etc.
    :param list_of_qubits: labels of qubits

    :return: string label for qubits

     NOTE: this function is "inverse operation" to get_qubit_indices_from_keystring.
    """

    if list_of_qubits is None:
        return None
    return 'q' + 'q'.join([str(s) for s in list_of_qubits])

#MOVE_TO >> core.utils core.numerics
def all_possible_bitstrings_of_length(number_of_bits: int,
                reversed: Optional[bool] = False):
    """Generate outcome bitstrings for n-qubits.

    Args:
        number_of_qubits (int): the number of qubits.

    Returns:
        list: arrray_to_print list of bitstrings ordered as follows:
        Example: n=2 returns ['00', '01', '10', '11'].
"""
    if (reversed == True):
        return [(bin(j)[2:].zfill(number_of_bits))[::-1] for j in list(range(2 ** number_of_bits))]
    else:
        return [(bin(j)[2:].zfill(number_of_bits)) for j in list(range(2 ** number_of_bits))]

#MOVE_TO >> core.utils core.numerics (PP) core.utils.DitConverter
#(PP): compare with povmtools version and usage across package
#(PP): change name to bitstring inside
def get_classical_register_bitstrings(qubit_indices: List[int],
                                      quantum_register_size: Optional[int] = None,
                                      rev: Optional[bool] = False):
    """
    Register of qubits of size quantum_register_size, with only bits corresponding to qubit_indices
    Gets list of bitstrings of length quantum_register_size when only bits in qubit_indicies can be 0 and 1, others have to be 0

    Qubits indices are always indexed from right to get proper output, use ref if you need a format with indexing from left.

    use rev when input indices were 


    varying

    :param qubit_indices:
    :param quantum_register_size:
    :param rev:
    :return:
    """

    # TODO FBM: refactor this function.

    # again assumes that qubit_indices contains unique values
    if quantum_register_size is None:
        quantum_register_size = len(qubit_indices)

    if quantum_register_size == 0:
        return ['']

    if quantum_register_size == 1:
        return ['0', '1']

    all_bitstrings= all_possible_bitstrings_of_length(quantum_register_size, rev)
    not_used = []

    for j in list(range(quantum_register_size)):
        if j not in qubit_indices:
            not_used.append(j)

    bad_names = []
    for bitstring in all_bitstrings: #0000111
        for k in (not_used):
            rev_name = bitstring[::-1] #1110000 reverses order of string - why?
            if rev_name[k] == '1':
                bad_names.append(bitstring)

    relevant_names = []
    for bitstring in all_bitstrings:
        if bitstring not in bad_names:
            relevant_names.append(bitstring)

    return relevant_names

#MOVE_TO >> core.utils core.numerics (PP) core.utils.DitConverter
def register_names_qubits(qubit_indices: List[int],
                          quantum_register_size: Optional[int] = None,
                          rev: Optional[bool] = False):
    # depreciated
    return get_classical_register_bitstrings(qubit_indices=qubit_indices,
                                             quantum_register_size=quantum_register_size,
                                             rev=rev)

#MOVE_TO >> core.utils? DELETE
def convert_qubits_string_to_tuple(qubits_string):
    return tuple(get_qubit_indices_from_keystring(qubits_string))
    
#MOVE_TO >> core.constans core.backends
def get_historical_experiments_number_of_qubits(backend_name: str):
    if backend_name == 'ibmq_16_melbourne':
        number_of_qubits = 15
    elif backend_name == 'ASPEN-8':
        number_of_qubits = 23
    elif backend_name.upper() == 'ASPEN-9':
        number_of_qubits = 20
    else:
        raise ValueError('Wrong backend name')

    return number_of_qubits

     


# =======================================================================================
# NUTILS
# =======================================================================================

#(PP): DELETE, should be removed from package everywhere it is used (no human input needed rule)
def query_yes_no(question):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    yes_answers = {'yes',
                   'y',
                   'ye',
                   'tak',
                   'sure',
                   'of course',
                   'Yes',
                   'yeah'}
    no_answers = {'no',
                  'n',
                  'nope',
                  'nah',
                  'nie',
                  'noo',
                  'nooo',
                  'noooo',
                  'No'}

    choice = 0
    print(question + ' [y/n] ')
    choice = input().lower()
    if choice in yes_answers:
        return True
    elif choice in no_answers:
        return False
    else:
        qprint('Please:', "respond with 'yes' or 'no'")
        return query_yes_no(question)

#MOVE_TO >> core.utils, REMOVE
def enumerate_dict(some_list: List[int]):
    ''' This function takes in a list 'some_list' and returns a dictionary where the keys are the indices of the elements in 'some_list' 
    and the values are the elements themselves.
    '''
    # TODO FBM: think whether the difference between this implementation and used one matters
    # def enumerate_dict(some_list):
    #     return dict((sorted_i, true_j) for sorted_i, true_j in enumerate(some_list))
    return dict(enumerate(some_list))

#MOVE_TO >> core.utils
#ORGANIZE: this function in constrast to the one above appears to be used (MO)
def wrapped_multiprocessing_function(tuple_of_main_arguments: List[tuple],
                                     additional_kwargs: dict,
                                     function_to_multiprocess: Callable,
                                     number_of_threads: Optional[int] = None,
                                     # debug=False,
                                     printing=False):
    """

    :param tuple_of_main_arguments:

    This is list of tuples that is divided into batches that are passed to different threads of
    multiprocessing. This, therefore should be set of VARIABLE arguments that are passed to the
    function of interest

    :param additional_kwargs:
    This is dictionary of arguments that are CONSTANT for all function evaluations.
    The dictionary is COPIED for each thread and passed to the function.


    :param function_to_multiprocess:
    :param number_of_threads:
    :return:
    """

    if number_of_threads is None:
        number_of_threads = int(
            np.min([multiprocessing.cpu_count() - 1, len(tuple_of_main_arguments)]))

    length = len(tuple_of_main_arguments)
    # print(length)
    # raise KeyboardInterrupt
    # IF there is less arguments than threads, we reduce number of threads
    if length < number_of_threads:
        number_of_threads = length


    division_cores = length // number_of_threads

    all_indices, arguments = [], []
    for process_pool_index in range(number_of_threads):
        if process_pool_index == number_of_threads - 1:
            slice_now = slice(process_pool_index * division_cores,
                              -1)
        else:
            slice_now = slice(process_pool_index * division_cores,
                              (process_pool_index + 1) * division_cores)
        sample_indices_now = tuple_of_main_arguments[slice_now]
        arguments.append((sample_indices_now,
                          additional_kwargs))

    if printing:
        qprint(f'Running {number_of_threads} threads!', '', 'green')

    pool = multiprocessing.Pool(number_of_threads)
    results = pool.starmap_async(function_to_multiprocess,
                                 arguments)
    pool.close()
    pool.join()

    res_multiprocessing = results.get()

    results_dictionary_all = {}

    for dict_now in res_multiprocessing:
        results_dictionary_all = {**results_dictionary_all, **dict_now}

    return results_dictionary_all 




# ORGANIZE - this function is only used in function get_reversed_enumerated_from_indices (MO)
#MOVE_TO >> core.utils
# WARNING: (PP) are the dictionary values unique?
def swap_keys_and_values(enumerated_dict: Dict[int, int]) -> Dict[int, int]:
    """
   This function takes in a dictionary 'enumerate' where the keys are integers and the values are also integers. 
   It returns a new dictionary where the keys and values are reversed from the input dictionary
    :param enumerate:
    :return:
    """
    reversed_map = {}
    for index_sorted, true_index in enumerated_dict.items():
        if true_index in reversed_map:
            raise warnings.warn(f"# WARNING # Value in the list repeats itself. Would silently merge and discard this element. Maybe should be like that?")
        reversed_map[true_index] = index_sorted
    return reversed_map

# MOcomm, PP - this name should reflect what is used
#MOVE_TO >> core.utils core.bitstrings
# TODO_MO (PP) are this global_indices? why are we using it like that?
# (PP) output hint and inputs type are not consistent int vs str
def get_reversed_enumerated_from_indices(indices: List[int]) -> Dict[str, int]:
    """
    Given indices list, enumerate them and return map which is inverse of enumerate
    :param indices:
    :return:
    """
    return swap_keys_and_values(enumerate_dict(indices))



# =======================================================================================
# PRINTER
# =======================================================================================



#MOVE_TO >> DELETE? - used in save_results_pickle
def gate_proper_date_string():
    ct0 = str(dt.datetime.today())
    ct1 = str.replace(ct0, ':', '_')
    ct2 = str.replace(ct1, '.', '_')
    ct3 = str.replace(ct2, '-', '_')
    return ct2[0:19]

#MOVE_TO >> DELETE? - used in save_results_pickle
def get_date_string(connector='_'):
    ct0 = str(dt.datetime.today())

    ct1 = str.replace(ct0, ':', connector)
    ct2 = str.replace(ct1, '.', connector)
    ct3 = ct2[0:10]

    return ct3




# =======================================================================================
# IO FILESYSTEM
# =======================================================================================
#MOVE_TO >> core.io
def get_module_directory():
    import __init__
    name_holder = __init__.__file__

    return name_holder[0:-11]

#MOVE_TO >> core.io
def get_local_storage_directory():
    # please create the environment variable in your virtual environment!
    # print(get_local_storage_directory())
    # print(os.listdir(os.environ['LOCAL_STORAGE_LOCATION']))
    # print(os.environ.keys())

    return os.environ['LOCAL_STORAGE_LOCATION']


#MOVE_TO >> core.io
def open_file_pickle(file_path):
    with open(file_path, 'rb') as filein:
        data_object = pickle.load(filein)

    return data_object

#(PP) delete not used - maybe better than above?
def quick_unpickle(filename):
    import pickle
    """
    Quickly load data from a pickle file.
    """

    if filename[-4:] != '.pkl':
        filename = filename + '.pkl'

    try:
        with open(filename, 'rb') as f:
            unpickled = pickle.load(f)
    except(ValueError):
        with open(filename, 'rb') as f:
            unpickled = pickle.load(f)

    return unpickled

#MOVE_TO >> core.io TO DELETE PP CAN BE A MARKER FOR UNUSED STUFF
def save_results_pickle(dictionary_to_save: dict,
                        directory: str,
                        custom_name: Optional[str] = None,
                        get_cwd: Optional[bool] = False):
    if (directory != None):
        #!?! add / at the end ...
        fp0 = [s for s in directory]
        if (fp0[len(fp0) - 1] != '/'):
            fp0.append('/')
        fp = ''.join(fp0)
    else:
        fp = ''
    # Time& date
    if (get_cwd):
        cwd = os.getcwd()
    else:
        cwd = ''
    ct3 = gate_proper_date_string()
    # original_umask = os.umask(0)
    # os.umask(original_umask)

    main_directory = cwd + fp

    # permission_mode=int('0777',8)
    # os.chmod(main_directory,permission_mode)
    check_dir = os.path.exists(main_directory)

    if (check_dir == False):
        try:
            os.makedirs(main_directory)

        except(FileExistsError):
            import shutil
            try:
                shutil.rmtree(main_directory)
                os.makedirs(main_directory)
            except(FileExistsError):
                os.makedirs(main_directory)

        print( Fore.CYAN + Style.BRIGHT + 'Attention: ' + Style.RESET_ALL + 'Directory ' + '"' + main_directory + '"' + ' was created.')
        # os.umask(oldmask)
        # os.chmod(main_directory,permission_mode)
    if custom_name is None:
        file_path = str(main_directory + 'Results_Object' + '___' + str(ct3))
    else:
        file_path = str(main_directory + custom_name)

    # os.chmod(main_directory)
    dict_results = dictionary_to_save

    add_end = ''

    if (file_path[len(file_path) - 4:len(file_path)] != '.pkl'):
        add_end = '.pkl'

    with open(file_path + add_end, 'wb') as f:
        pickle.dump(dict_results, f, pickle.HIGHEST_PROTOCOL)


# =======================================================================================
# OTHER
# =======================================================================================
#MOVE_TO >> core.math
# TODO_MO compare with get_random_stochastic_matrix_1q - multiple implementations?
# delete the 1q version of random stochastic matrix in favour of this with size = 2
def random_stochastic_matrix(size, type='left'):
    matrix = np.random.rand(size, size)

    if (type == 'left'):
        matrix = matrix / matrix.sum(axis=0)[None, :]
    elif (type == 'right'):
        matrix = matrix / matrix.sum(axis=1)[:, None]
    elif (type == 'doubly' or type == 'double' or type == 'orto'):
        matrix = matrix = matrix / matrix.sum(axis=0)[None, :]
        matrix = matrix / matrix.sum(axis=1)[:, None]

    return matrix


#(PP) what is abstract_format?
#(PP) TODO_JT, TODO_MO not sure where to put - probably somewhere to io?
def create_batches(circuits_list, circuits_per_job):
    '''
    Function creating list of batches in abstract format. It takes the following inputs
        circuits list - list with tomographic circuits
        circuits_per_job - number of circuits in a batch 
    '''

    total_number_of_circuits = len(circuits_list)

    #computes total number of batches
    number_of_jobs = int(np.ceil(total_number_of_circuits / circuits_per_job))

    #initializes baches set
    batches = []
    #iteration over batches_index and creation of baches of size 
    for batch_index in range(number_of_jobs):
        circuits_now = circuits_list[batch_index * circuits_per_job : (batch_index + 1) * circuits_per_job] 
        batches.append(circuits_now)
    return batches
    # Because of how python treats lists/ arrays the last bach has automatically the right size (of the remaining circuits)



















# =======================================================================================
# CANDIDATES TO BE DELETED BELOW
# =======================================================================================

#MOVE_TO >> core.utils / duplicate
# #ORGANIZE - this function is used only once for some flder opeprations (MO)
# def get_drive_path():
#     try:
#         return os.environ['LOCAL_DRIVE_DIRECTORY']
#     except(KeyError):
#         return os.environ['LOCAL_STORAGE_LOCATION']


#MOVE_TO >>  DELETE
# def generate_classical_register_bistrings_product(clusters_list: List[Tuple[int]]):
#     clusters_lengths = [len(cl) for cl in clusters_list]
#     if np.max(clusters_lengths) > 15:
#         raise ValueError(f"Too big cluster with size {np.max(clusters_lengths)}")

#     # number_of_qubits = sum(clusters_lengths)

#     local_registers = {cluster: get_classical_register_bitstrings(qubit_indices=range(len(cluster)))
#                        for cluster in clusters_list}
#     # for cluster in clusters_list:
#     #     register_cluster =
#     #     local_registers.append([(cluster, x) for x in register_cluster])
#     #
#     # cartesian_product = itertools.product(local_registers)
#     #
#     # bitstrings_list = []
#     #
#     # for bitstrings_list_with_cluster in cartesian_product:
#     #     bitstring_global = ['0' for _ in range(number_of_qubits)]
#     #     print(bitstrings_list_with_cluster[0])
#     #     for cluster, bitstring_local in bitstrings_list_with_cluster[0]:
#     #         # print(cluster, bitstring_local)
#     #         for index in range(len(bitstring_local)):
#     #             bitstring_global[cluster[index]] = bitstring_local[index]
#     #
#     #     bitstrings_list.append(bitstring_global)
#     return local_registers



#(PP)ORGANIZE - this function is i) trivial and ii)  nerer used - a cleare candidate for deletion  
#def decompose_qubit_matrix_in_pauli_basis(matrix):
#    return {pauli_label: 1 / 2 * np.trace(matrix @ pauli_matrix)
#            for pauli_label, pauli_matrix in pauli_sigmas.items()}

# def get_bell_basis():
#     return list(___bell_states___.values())


#(PP)ORGANIZE - this class is not used anywhere - and hence it is a candidate for deletion (MO)
# (PP) Also, what class does in the function folder?

# class key_dependent_dict(defaultdict):
#     """
#     This is class used to construct dictionary which creates values of keys in situ, in case there
#     user refers to key that is not present.

#     COPYRIGHT NOTE
#     This code was taken from Reddit thread:
#     https://www.reddit.com/r/Python/comments/27crqg/making_defaultdict_create_defaults_that_are_a/

#     """

#     def __init__(self, f_of_x=None):
#         super().__init__(None)  # base class doesn't get a factory
#         self.f_of_x = f_of_x  # save f(x)

#     def __missing__(self, key):  # called when a default needed
#         ret = self.f_of_x(key)  # calculate default value
#         self[key] = ret  # and install it in the dict
#         return ret


#ORGANIZE: this function does not appear anywther - candidate for deletion

#def get_time_now():
#    ct0 = str(dt.datetime.today())     #MO: in this lane I replaced datetime.datetime.today() to dt.datetime.today() need to return to previous verion if does not work
#    ct1 = str.replace(ct0, ':', '_')
#    ct2 = str.replace(ct1, '.', '_')
#    ct3 = ct2[0:19]
#
#    return ct3



#ORGANIZE: this function does not appear anywther - candidate for deletion (MO)

#def wrapped_multiprocessing_function_depreciated(tuple_of_main_arguments: List[tuple],
#                                                 additional_kwargs: dict,
#                                                 function_to_multiprocess: Callable,
#                                                 number_of_threads: Optional[int] = None,
#                                                 # debug=False,
#                                                 printing=False):
#    """
#
#    :param tuple_of_main_arguments:
#
#    This is list of tuples that is divided into batches that are passed to different threads of
#    multiprocessing. This, therefore should be set of VARIABLE arguments that are passed to the
#    function of interest
#
#    :param additional_kwargs:
#    This is dictionary of arguments that are CONSTANT for all function evaluations.
#    The dictionary is COPIED for each thread and passed to the function.
#
#
#    :param function_to_multiprocess:
#    :param number_of_threads:
#    :return:
# """         if number_of_threads is None:
#         number_of_threads = int(
#             np.min([multiprocessing.cpu_count() - 1, len(tuple_of_main_arguments)]))

#     length = len(tuple_of_main_arguments)

#     # IF there is less arguments than threads, we reduce number of threads
#     if length < number_of_threads:
#         number_of_threads = length

#     division_cores = length // number_of_threads

#     all_indices, arguments = [], []

#     # if debug:
#     # print(length, division_cores)

#     for process_pool_index in range(number_of_threads):
#         if process_pool_index == number_of_threads - 1:
#             slice_now = slice(process_pool_index * division_cores,
#                               -1)
#         else:
#             slice_now = slice(process_pool_index * division_cores,
#                               (process_pool_index + 1) * division_cores)

#         sample_indices_now = tuple_of_main_arguments[slice_now]
#         arguments.append((sample_indices_now,
#                           additional_kwargs))

#     # if debug:
#     #     raise KeyError
#     if printing:
#         qprint(f'Running {number_of_threads} threads!', '', 'green')
#     pool = multiprocessing.Pool(number_of_threads)
#     results = pool.starmap_async(function_to_multiprocess,
#                                  arguments)
#     pool.close()
#     pool.join()

#     res_multiprocessing = results.get()

#     results_dictionary_all = {}

#     for dict_now in res_multiprocessing:
#         results_dictionary_all = {**results_dictionary_all, **dict_now}

#     # last_run_indices = list(range(int(division_cores * number_of_threads), length))
#     # last_mp = [([tuple_of_main_arguments[x]], additional_kwargs) for x in last_run_indices]

#     # if debug:
#     #     print('hey bro', last_run_indices, len(last_run_indices))

#     return results_dictionary_all

# """


#ORGANIZE - the function below is not used throughout the project - I commented it out (MO)

#def try_to_do_something_multiple_times(what_to_do: Callable,
#                                       print_string: str,
#                                       how_many_tries=1000):
    # """
    # Codes try to run "what_to_do" callable "how_many_tries" times,
    # waiting 10 seconds each time there is an error.

    # :param what_to_do:
    # :param print_string:
    # :return:
    # """

#    for error_counter in range(how_many_tries):
#        try:
#           return what_to_do()
#        except:
#            print(
#                f"WARNING: An error occurred for experiment: '{print_string}'.")
#            traceback.print_exc()
#
 #       print(f"Waiting {10}s.")
  #      time.sleep(10)
   #     print(f"Retrying experiment: '{print_string}'.")
#
#        if (error_counter + 1) % 25 == 0:
#            qprint(
#                f"\n\nAlready tried '{print_string}' {str(error_counter)} times! Something seems to be wrong...\n\n",
#                '',
#                'red')