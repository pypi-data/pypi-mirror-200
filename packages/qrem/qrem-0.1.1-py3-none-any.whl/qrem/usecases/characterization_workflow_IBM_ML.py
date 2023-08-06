import sys
import os
import numpy as np
import pickle

from qiskit import IBMQ

operating_system = 'LIN'

if operating_system=='WIN':
    directory_QREM = os.environ["QREM"] +'\\'
    data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data'
elif operating_system=='LIN':
    directory_QREM = '/home/fbm/PycharmProjects/QREM_SECRET_DEVELOPMENT/'
    data_directory = '/home/fbm/Nextcloud/Theory of Quantum Computation/QREM_Data/ibm/'
sys.path.append(os.path.dirname(directory_QREM))

from qrem.noise_characterization.tomography_design.overlapping.QDTMarginalsAnalyzer import QDTMarginalsAnalyzer
from qrem.functions_qrem import ancillary_functions as anf
from qrem.noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer

import qrem.common.math as qrem_math





results_file ='QDOT_counts_IBM_WAS_281122'

with open(data_directory+results_file+'.pkl', 'rb') as filein:
    results_data_dictionary = pickle.load(filein)

results_dictionary = results_data_dictionary['results_dictionary']
metadata = results_data_dictionary['metadata']
print(len(metadata['physical_qubits']))

locality=2
subset_of_qubits = qrem_math.get_k_local_subsets(number_of_elements=len(metadata['physical_qubits']), 
                                                 subset_size=locality,
                                                 all_sizes_up_to_k = True)



file_name_marginals = 'QDOT_marginals_IBM_WAS_281122'
with open(data_directory+file_name_marginals +'.pkl', 'rb') as filein:
    marginals_data_dictionary = pickle.load(filein)

marginals_dictionary = marginals_data_dictionary['marginals_dictionary']






marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name='QDT',marginals_dictionary=marginals_dictionary)

marginals_analyzer.initialize_labels_interpreter(interpreter='PAULI')

#calculate reduced POVMs
marginals_analyzer.compute_subsets_POVMs_averaged(subsets_of_qubits =subset_of_qubits,
                                                           show_progress_bar=True,
                                                           estimation_method='ML')
POVMs_dictionary = marginals_analyzer._POVM_dictionary

dictionary_to_save = {'metadata':metadata,
                     'POVMs_dictionary':POVMs_dictionary}


file_name_POVMs  = 'QDOT_POVMs_ML_IBM_WAS_281122.pkl'

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
distances_types_correlations = [('worst_case', 'classical')]
                #,('average_case', 'classical')
                 # ,('worst_case', 'quantum'),
                 # ('average_case', 'quantum')]
#Tell analyzer how to interpret labels of circuits. For now we can only use Pauli overcomplete basis.
noise_analyzer.compute_correlations_data_pairs(qubit_indices=range(len(metadata['physical_qubits'])),
                                              distances_types=distances_types_correlations)

correlations_data = noise_analyzer.correlations_data

dictionary_to_save = {'correlations_data':correlations_data,
                      'metadata':metadata
                     }

file_name_errors  = 'QDOT_correlations_ML_IBM_WAS_281122.pkl'
anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_errors)
