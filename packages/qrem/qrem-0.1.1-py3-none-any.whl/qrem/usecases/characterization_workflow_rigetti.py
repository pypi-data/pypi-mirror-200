import sys
import os

import numpy as np
import pickle
from qiskit import IBMQ


#--------------------------------------------------------
#(PP) Janknu, umówimy się na jakieś spokojne spotkanie, pokażę Ci kilka fajnych rozwiązań jak
# ja podchodzę do pisania skryptów typu "usecase" -  
operating_system = 'LIN'
if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/JM/braket_rigetti_experiments_12-2022/'
sys.path.append(os.path.dirname(directory_QREM))
#--------------------------------------------------------

from qrem.functions_qrem import ancillary_functions as anf
from qrem.functions_qrem import functions_data_analysis as fdt

from qrem.noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer
from qrem.noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import QDTMarginalsAnalyzer

import qrem.common.math as qrem_math



results_file ='QDOT_2022-12-22_processed_results'
metadata_file = '2022-12-22_metadata_whole_script_test'

with open(data_directory+results_file+'.pkl', 'rb') as filein:
    results_dictionary = pickle.load(filein)


with open(data_directory+metadata_file+'.pkl', 'rb') as filein:
    metadata = pickle.load(filein)

metadata = metadata['metadata']
print(len(metadata['physical_qubits']))

locality=2
subset_of_qubits = qrem_math.get_k_local_subsets(number_of_elements=len(metadata['physical_qubits']), 
                                                 subset_size=locality,
                                                 all_sizes_up_to_k = True)

# here the uusage of this class i ragther limitted - we could use base class instead
marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name='QDT')
print('Calculation starts')
marginals_analyzer.compute_all_marginals(subsets_of_qubits=  subset_of_qubits,show_progress_bar=True,multiprocessing=True)

marginals_dictionary = marginals_analyzer.marginals_dictionary

print('done')

dictionary_to_save = {'metadata':metadata,
                    'marginals_dictionary':marginals_dictionary}

device_name = metadata['backend_name']
experiment_date = metadata['date']
file_name_marginals = 'QDOT_marginals_'+device_name + '_' + experiment_date




anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_marginals)

with open(data_directory+file_name_marginals+'.pkl', 'rb') as filein:
    marginals_data_dictionary = pickle.load(filein)

marginals_dictionary=marginals_data_dictionary['marginals_dictionary']

#MOcomm  why do we initialize marginals_analyzer twiece?
marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name='QDT',marginals_dictionary=marginals_dictionary)

marginals_analyzer.initialize_labels_interpreter(interpreter='PAULI')

#calculate reduced POVMs
marginals_analyzer.compute_subsets_POVMs_averaged(subset_of_qubits,
                                                           show_progress_bar=True,
                                                           estimation_method='PLS')
# we are getting here a private variable of an object...
POVMs_dictionary = marginals_analyzer._POVM_dictionary

dictionary_to_save = {'metadata':metadata,
                     'POVMs_dictionary':POVMs_dictionary}


file_name_POVMs  = 'QDOT_POVMs_PLS_'+device_name + '_' + experiment_date


#why do we initialize another element of characterization class?
noise_analyzer = InitialNoiseAnalyzer(results_dictionary,
                                      marginals_dictionary=marginals_dictionary,
                                      POVM_dictionary=POVMs_dictionary
                                              )

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_POVMs)

#Specify what qubits are of interest to you (here default is all of them)
qubit_indices = list(range(len(metadata['physical_qubits'])))

#Specify what types of distances you want to calculate
distances_types_correlations = [('worst_case', 'classical'),
                   ('average_case', 'classical')
                  ,('worst_case', 'quantum'),
                  ('average_case', 'quantum')]
#Tell analyzer how to interpret labels of circuits. For now we can only use Pauli overcomplete basis.
noise_analyzer.compute_correlations_data_pairs(qubit_indices=range(len(metadata['physical_qubits'])),
                                              distances_types=distances_types_correlations)

correlations_data = noise_analyzer.correlations_data

dictionary_to_save = {'correlations_data':correlations_data,
                      'metadata':metadata
                     }

file_name_errors  = 'QDOT_correlations_'+device_name + '_' + experiment_date
anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_errors)
