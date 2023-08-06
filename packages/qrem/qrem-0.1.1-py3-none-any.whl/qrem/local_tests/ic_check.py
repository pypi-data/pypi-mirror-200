import sys
import os
import pickle





directory_QREM = os.environ["QREM"] +'\\src\\qrem\\'
sys.path.append(os.path.dirname(directory_QREM))

from qrem.functions_qrem import information_completeness_check as icc

#input data: some data with strings corresponding to settings of tomographic circuits collection (here marginals dictionary, can be just a list of settings)
data_directory = 'C:\\Users\\Enter\\Nextcloud2\\Theory of Quantum Computation\\QREM_Data\\rigetti\\'

file_name = 'QDOT_marginals_ASPEN-M-2_2022-12-22.pkl'


with open(data_directory+file_name, 'rb') as filein:
    results_data = pickle.load(filein)

#creation of symbols list, for which a check performed (a list ['0',...,'5'] for QDOT and ['0','1'] for DDOT, can be hidden inside the function and additional list can be provided by the user if needed)
QDOT_symbol_list =[str(i) for i in range(6)]
DDOT_symbol_list =[str(i) for i in range(2)]

circuits_list = list(results_data['marginals_dictionary'].keys())

"""
Function checking how many times a particular input setting to measurement tomography protocol is realized in a given set of circuits for all subsets of qubits of a fixed locality

Parameters
----------
tomographic_circuits_list : list
    the list of circuits that are used for measurement tomography protocol 

locality : int
    number corresponding to locality of subsets for which information completness check is performed  

symbol_string : string
    list of strings of symbols used to encode input settings, e.g. for 6 state overcomplete Pauli basis it's ['0','1','2','3','4','5']

Returns
-------
symbols_subset_dictionary: dictionary
    a dictionary with keys of a form ((subset_of_qubits),input_setting) (e.g. ((0,1),'50')  and values corresponding to the number of times that a given input_setting is realized for this particular subset

missing_symbols: dictionary
    a dictionary with keys corresponding to qubit_subsets (e.g. (0,1)) and values corresponding to list of settings that don't appear for a given subset e.g. ['00','15']


"""
symbols_dictionary, missing_symbols = icc.information_completeness_verification_quantitative(tomographic_circuits_list=circuits_list,locality=2,symbol_string_list=QDOT_symbol_list)


print(missing_symbols)