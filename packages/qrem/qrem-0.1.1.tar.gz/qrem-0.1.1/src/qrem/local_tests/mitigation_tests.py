import sys
import os
import random
import pickle 

from tqdm import tqdm
import numpy as np

directory_QREM = os.environ["QREM"] +'\\src\\qrem\\'
data_directory = 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\test_data\\'
sys.path.append(os.path.dirname(directory_QREM))

import qrem.functions_qrem.ancillary_functions  as anf
import qrem.functions_qrem.functions_data_analysis as fdt 

from qrem.noise_characterization.tomography_design.overlapping.DOTMarginalsAnalyzer import DOTMarginalsAnalyzer  
from qrem.noise_characterization.base_classes.OverlappingTomographyBase import OverlappingTomographyBase
from qrem.noise_characterization.tomography_design.overlapping.SeparableCircuitsCreator import SeparableCircuitsCreator
from qrem.noise_characterization.data_analysis.InitialNoiseAnalyzer import InitialNoiseAnalyzer

from qrem.backends_support.qiskit import qiskit_utilities
from qrem.functions_qrem import functions_data_analysis as fdt

from qrem.noise_simulation.CN.noise_implementation import  simulate_noise_results_dictionary
from qrem.noise_model_generation.CN.NoiseModelGenerator import NoiseModelGenerator

import qrem.common.math as qrem_math
from qrem.common.printer import qprint, qprint_array
from qrem.functions_qrem import functions_benchmarks as fun_ben
from qrem.local_tests import marginals_correction_tests_functions as test_fun 

from datetime import date 
def TVD(p,q):
    tvd = 0
    for el1,el2 in zip(p,q):
        tvd+=np.abs(el1-el2)
    return 0.5*tvd 

# Function used to divide a dictionary into two parts. Here it is used to create characterization and benchmark data 

def divide_dictionary(dictionary, items_number, start_index=0):
    counter=0
    divided_dictionary_1 ={}
    divided_dictionary_2={}
    for key,entry in  dictionary.items():
        if counter<start_index+items_number-1:
            divided_dictionary_1[key] = entry
        else:
            divided_dictionary_2[key]=entry    
        counter=counter+1
    return divided_dictionary_1, divided_dictionary_2


'''
A function used to divide qubits into clusters 

input parameters:  


qubit_indices - a list of qubit indices 

clusters_specification - a nested list contaning description of clusters to be created:

        structure of the list [[element_1, element_2], ...]:
            element_1 - integer encoding locality of a cluster
            element_2 - number of clusters of given locality
        
        e.g. [[3,1],[2,2]] encodes 1 3 qubit cluster and two 2 qubit clusters

output parameters: 
    cluster_list a list with qubits assigned to clusters

    cluster      

'''
def divide_qubits_in_the_clusters(qubit_indices, clusters_specification):
    qubit_indices_now=qubit_indices
    cluster_list = []
    cluster_now =[]
    # a loop over 
    for el in clusters_specification:
        
        #a sublist of tot
        cluster_now=random.sample(list(qubit_indices_now), el[0]*el[1] )
        qubit_indices_now = set(qubit_indices_now) - set(cluster_now)
        cluster_now.sort()
        cluster_now=[tuple(cluster_now[i:i+el[0]]) for i in range(0,el[0]*el[1],el[0])]
        for element in cluster_now:
            cluster_list.append(element)
    return cluster_list


#Workflow starts
#specify number of qubits

number_of_qubits = 10

#a string used to specify name of files useed to save data

name_string = str(date.today()) + " q" + str(number_of_qubits) 



qubit_indices = [i for i in range(number_of_qubits)]


OT_creator = OverlappingTomographyBase(number_of_qubits=number_of_qubits, experiment_name='DDOT') 
                                       

circuits_QDOT = OT_creator.get_random_circuits_list(number_of_circuits=1200)
        

    

circuits_creator = SeparableCircuitsCreator(SDK_name='qiskit', 
                                            qubit_indices=qubit_indices,
                                            descriptions_of_circuits=circuits_QDOT,
                                            experiment_name='DDOT')

OT_circuits_list = circuits_creator.get_circuits()

batches = anf.create_batches(circuits_list=OT_circuits_list, circuits_per_job = 300)

jobs_list = qiskit_utilities.run_batches(backend_name='qasm_simulator',batches=batches, shots=10**4)

unprocessed_results = qiskit_utilities.get_counts_from_qiskit_jobs(jobs_list=jobs_list)

processed_results = fdt.convert_counts_overlapping_tomography(counts_dictionary=unprocessed_results, experiment_name='DDOT')


file_name_results  = 'DDOT_simulation_workflow_results_' + name_string +'.pkl'
anf.save_results_pickle(dictionary_to_save=processed_results,
                                directory=data_directory,
                                custom_name=file_name_results)










        

#specify number of different clusters 
cluster_list = divide_qubits_in_the_clusters(qubit_indices=qubit_indices,clusters_specification=[[3,1],[2,3],[1,1]])


#create noise dictionary
noise_model_dictionary ={}
for element in cluster_list:
    noise_model_dictionary[element] = {'averaged':anf.random_stochastic_matrix(2**len(element))}


marginals_analyzer_ideal = DOTMarginalsAnalyzer(results_dictionary_ddot=processed_results)

marginals_analyzer_ideal.compute_all_marginals(cluster_list,show_progress_bar=True,multiprocessing=False)

ideal_experiments_dic, ideal_benchmarks_dic = divide_dictionary(marginals_analyzer_ideal.marginals_dictionary,len(marginals_analyzer_ideal.marginals_dictionary.keys())-49)



#simulate readout noise 
noisy_results_dictionary=simulate_noise_results_dictionary(processed_results,noise_model_dictionary)

file_name_noise_model  = 'DDOT_simulation_workflow_noise_model_' + name_string+ '.pkl'
anf.save_results_pickle(dictionary_to_save=noise_model_dictionary,
                                directory=data_directory,
                                custom_name=file_name_noise_model)

file_name_noisy_results  = 'DDOT_noisy_simulation_results_' + name_string +'.pkl'

anf.save_results_pickle(dictionary_to_save=noisy_results_dictionary,
                                directory=data_directory,
                                custom_name=file_name_noisy_results)

print('Simulation of noise is finished')

locality=2
subset_of_qubits = qrem_math.get_k_local_subsets(number_of_qubits, 2)




print('Marginals calculation starts')

marginals_analyzer = DOTMarginalsAnalyzer(results_dictionary_ddot=noisy_results_dictionary)


marginals_analyzer.compute_all_marginals(subset_of_qubits,show_progress_bar=True,multiprocessing=False)

marginals_dictionary=marginals_analyzer.marginals_dictionary










dictionary_to_save = {'marginals_dictionary':marginals_dictionary}




file_name_marginals = 'DDOT_marginals_workflow_' + name_string +'.pkl'

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_marginals)

#with open(data_directory+file_name_marginals +'.pkl', 'rb') as filein:
#    results_data_dictionary = pickle.load(filein)

#marginals_dictionary = results_data_dictionary['marginals_dictionary']
anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_marginals)

print('Marginals calculation is finished')


print('POVM calculation starts')
marginals_analyzer.compute_subset_noise_matrices_averaged(subset_of_qubits)

#marginals_analyzer = QDTMarginalsAnalyzer(results_dictionary,experiment_name="DDOT",marginals_dictionary=marginals_dictionary)
#marginals_analyzer.initialize_labels_interpreter(interpreter='PAULI')


#calculate reduced POVMs
#marginals_analyzer.compute_subsets_POVMs_averaged(subset_of_qubits,
#                                                           show_progress_bar=True,
#                                                           estimation_method='PLS')
POVMs_dictionary_diag= marginals_analyzer._noise_matrices_dictionary




file_name_POVMs  = 'DDOT_POVMs_PLS_workflow_' + name_string +'.pkl'

#POVMs are read from noise matricces (as diagonal matrices)


POVMs_dictionary = {}
for key, entry in POVMs_dictionary_diag.items():
    list_of_matrices=[]
    for matrix in POVMs_dictionary_diag[key]['averaged']:
        list_of_matrices.append(np.diag(matrix))

    POVMs_dictionary[key]=list_of_matrices

dictionary_to_save = {'POVMs_dictionary':POVMs_dictionary}

characterization_results_dictionary, benchmarks_results_dictionary=divide_dictionary(noisy_results_dictionary,len(noisy_results_dictionary.keys())-49)
characterization_results_dictionary = noisy_results_dictionary
characterization_marginals_dictionary, benchmarks_marginals_dictionary = divide_dictionary(marginals_dictionary,len(noisy_results_dictionary.keys())-49)
characterization_marginals_dictionary = marginals_dictionary
characterization_POVMs_dictionary=POVMs_dictionary

noise_analyzer = InitialNoiseAnalyzer(results_dictionary=characterization_results_dictionary,
                                      marginals_dictionary=characterization_marginals_dictionary,
                                      POVM_dictionary=characterization_POVMs_dictionary
                                              )

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_POVMs)

print('POVM calculation is finished')

#Specify what qubits are of interest to you (here default is all of them)
qubit_indices = list(range(number_of_qubits))

#Specify what types of distances you want to calculate
distances_types_correlations = [('worst_case', 'classical')]
        
#Tell analyzer how to interpret labels of circuits. For now we can only use Pauli overcomplete basis.
noise_analyzer.compute_correlations_data_pairs(qubit_indices=range(number_of_qubits),
                                              distances_types=distances_types_correlations)

correlations_data = noise_analyzer.correlations_data

dictionary_to_save = {'correlations_data':correlations_data,
                      
                     }

file_name_errors  = 'DDOT_correlations_workflow_' + name_string +'.pkl'
anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=data_directory,
                                custom_name=file_name_errors)



characterization_noise_matrix_dictionary = fdt.get_noise_matrices_from_POVMs_dictionary(characterization_POVMs_dictionary)




#read saved results
#with open(data_directory + file_name_errors+'.pkl', 'rb') as filein:
#    errors_data_dictionary = pickle.load(filein)

#errors_data = errors_data_dictionary['errors_data']
#coherence_data = errors_data_dictionary['coherence_data']
#correlations_data = errors_data_dictionary['correlations_data']


noise_model_analyzer = NoiseModelGenerator(results_dictionary=characterization_results_dictionary,
                                           marginals_dictionary=characterization_results_dictionary,
                                           noise_matrices_dictionary=characterization_noise_matrix_dictionary ,
                                           correlations_data=correlations_data
                                           )



sizes_clusters = [2,3]

distance_type = 'worst_case'
correlations_type = 'classical'
correlations_table = correlations_data[distance_type][correlations_type]

alpha_hyperparameters = np.linspace(0.0, 3.0, 16)
alpha_hyperparameters = [np.round(alpha, 3) for alpha in alpha_hyperparameters]
alpha_hyperparameters=[1]

all_clusters_sets_dictionary = {tuple([(qi,) for qi in range(number_of_qubits)]):None}


for max_cluster_size in sizes_clusters:
    print("\nCurrent max cluster size:", max_cluster_size, 'red')

    for alpha_multiplier in alpha_hyperparameters:
        clustering_function_arguments = {'alpha_multiplier': alpha_multiplier}

        clusters_tuples_now, score = noise_model_analyzer.compute_clusters(correlations_table=correlations_table,
                                                                           maximal_size=max_cluster_size,
                                                                           method_kwargs=clustering_function_arguments)
        if clusters_tuples_now in all_clusters_sets_dictionary.keys():
            all_clusters_sets_dictionary[clusters_tuples_now].append(
                (max_cluster_size, clustering_function_arguments['alpha_multiplier'], score))
        else:
            all_clusters_sets_dictionary[clusters_tuples_now] = [
                (max_cluster_size, clustering_function_arguments['alpha_multiplier'], score)]


all_clusters_sets_dictionary ={}

temp_list=[]
for key, items in noise_model_dictionary.items():
    key_temp = list(key)
    key_temp.sort()
    
    temp_list.append(tuple(key_temp))

all_clusters_sets_dictionary[tuple(temp_list)]=[(3,'ideal')]


all_clusters_sets_list = list(all_clusters_sets_dictionary.keys())

cluster_subsets = []

for cluster_list in all_clusters_sets_list:
    for cluster in cluster_list:
        if cluster not in cluster_subsets:
            cluster_subsets.append(cluster)

# Calculate chosen marginals
marginals_analyzer.compute_all_marginals(cluster_subsets,
                                         show_progress_bar=True,
                                         multiprocessing=False)

marginals_dictionary_clusters = marginals_analyzer.marginals_dictionary



marginals_analyzer.compute_subset_noise_matrices_averaged(subsets_list=cluster_subsets,show_progress_bar=True)

noise_matrices_dictionary = marginals_analyzer.noise_matrices_dictionary




dictionary_to_save = {'noise_matrices_dictionary': noise_matrices_dictionary,
                      'all_clusters_sets_dictionary': all_clusters_sets_dictionary
                      }

"""
Uncomment to save data 
"""

directory_results_noise_models = data_directory
file_name_noise_models  = "DDOT_clusters_workflow_" + name_string +'.pkl'

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory=directory_results_noise_models,
                                custom_name=file_name_noise_models)


pairs_of_qubits = [(i, j) for i in range(number_of_qubits) for j in range(i + 1, number_of_qubits)]

correction_matrices, correction_indices,mitigation_data_dictionary = fdt.get_multiple_mitigation_strategies_clusters_for_pairs_of_qubits(
    pairs_of_qubits=pairs_of_qubits,
    clusters_sets=all_clusters_sets_dictionary,
    dictionary_results=characterization_results_dictionary,
    noise_matrices_dictionary=noise_matrices_dictionary,
    show_progress_bar=True)

dictionary_to_save = {
                      'correction_matrices': correction_matrices,
                      'correction_indices': correction_indices,
                      'mitigation_data' : mitigation_data_dictionary,
                      'all_clusters_sets_dictionary': all_clusters_sets_dictionary
                      }

"""
Uncomment to save data 
"""
file_name_mitigation  = "DDOT_mitigation_workflow_" + name_string +'.pkl'

anf.save_results_pickle(dictionary_to_save=dictionary_to_save,
                                directory= data_directory,
                                custom_name=file_name_mitigation)




counter =0




results_name_marginals ='DDOT_marginals_benchmarks_workflow_' + name_string +'.pkl'

anf.save_results_pickle(dictionary_to_save=benchmarks_results_dictionary,
                                directory=data_directory,
                                custom_name=results_name_marginals)

results_name ='DDOT_results_benchmarks_workflow_' + name_string +'.pkl'

anf.save_results_pickle(dictionary_to_save=benchmarks_marginals_dictionary,
                                directory=data_directory,
                                custom_name=results_name)

correction_matrices_dictionary_new = mitigation_data_dictionary[all_clusters_sets_list[0]][1] 

correction_data_now = {'subsets_to_correct': all_clusters_sets_list[0],
                        'correction_matrices': correction_matrices_dictionary_new,
                         "correction_indices":correction_indices }
mitigation_method = 'lambda_inverse'
method_kwargs = {'ensure_physicality': True}

for subset,matrix in correction_matrices_dictionary_new.items():
    print(noise_matrices_dictionary[subset]['averaged'].dot(matrix))  



test_results=test_fun.correct_marginals_on_clusters(benchmarks_marginals_dictionary,benchmarks_results_dictionary,correction_data_now,method_kwargs,mitigation_method,pairs_of_qubits)

comparison_dict={}

tvd_list =[[],[]]
for state in ideal_benchmarks_dic.keys():
    comparison_dict={}
    for marginal in ideal_benchmarks_dic[state]:
        comparison_dict[tuple([state,marginal])] = TVD((test_results[state][marginal]).flatten(),ideal_benchmarks_dic[state][marginal])
     

#hamiltonians_dictionary=fun_ben.create_hamiltonians_for_benchmarks(number_of_qubits=number_of_qubits, number_of_hamiltonians=50, clause_density=4.0)

#file_name_hamiltonians  = "DDOT_hamiltonians_workflow_27022023"


#anf.save_results_pickle(dictionary_to_save=hamiltonians_dictionary,
#                                directory=data_directory,
#                                custom_name=file_name_hamiltonians)


#energy_dictionary= fun_ben.eigenstate_energy_calculation_and_estimation(benchmarks_results_dictionary,benchmarks_marginals_dictionary,hamiltonians_dictionary)








#run benchmars, a super ugly input to be changed later
#benchmarks_results, mitigated_marginals_dictionary=fun_ben.run_benchmarks(number_of_qubits,benchmarks_results_dictionary, benchmarks_marginals_dictionary, energy_dictionary, hamiltonians_dictionary,all_clusters_sets_dictionary,correction_matrices, correction_indices,mitigation_data_dictionary,noise_matrices_dictionary)

#comparison_dictionary = {}

#for state, marginals_dic in ideal_benchmarks_dic.items():
#    comparison_dictionary_total ={}
#    for subset, marg in marginals_dic.items():
#        comparison_dictionary[subset]=marg - mitigated_marginals_dictionary[state][subset]





#file_name_benchmark_results = 'DDOT_benchmarks_workflow_27022023'

#anf.save_results_pickle(dictionary_to_save=benchmarks_results,
#                                directory=data_directory,
#                                custom_name=file_name_benchmark_results)

#below analysis of benchmark results starts
#all_tested_clusters_sets = list(benchmarks_results[0]['energies']['predicted_energies'].keys())


#the code below rewrites benchmark results into spearate dictionaries for mitigation/prediction
#benchmark_results_prediction = {}
#for cluster_set in all_tested_clusters_sets:
#       benchmark_results_prediction[cluster_set] = {'errors_list': {
#       state_index: benchmarks_results[state_index]['errors']['energy_prediction_errors'][cluster_set] for
#       state_index in benchmarks_results.keys()}}


#all_tested_clusters_sets = list(benchmarks_results[0]['energies']['corrected_energies'].keys())

#benchmark_results_mitigation = {}
#for cluster_set in all_tested_clusters_sets:
#      benchmark_results_mitigation[cluster_set] = {
#      'errors_list': {state_index: benchmarks_results[state_index]['errors']['corrected_errors'][cluster_set] for
#      state_index in benchmarks_results.keys()}}

#division of hamiltonians into test and traning set

#traning_set,test_set= fun_ben.create_traning_and_test_set(number_of_hamiltonians=50, traning_set_cardinality=40)

#here one by choosig benchmark_results_mitigation/benchmark_results_prediction one can analyze mitigation/porediction
#traning_data_mitigation=fun_ben.calculate_results_test_set(benchmark_results_mitigation, traning_set)
#test_data_mitigation=fun_ben.calculate_results_test_set(benchmark_results_mitigation, test_set)

#traning_data_prediction=fun_ben.calculate_results_test_set(benchmark_results_prediction, traning_set)
#test_data_prediction=fun_ben.calculate_results_test_set(benchmark_results_prediction, test_set)

#this creates data for plots
#alpha_list, median_list_mitigation_traning, mean_list_mitigation_traning = fun_ben.cerate_data_alpha_plot(all_clusters_sets_dictionary,traning_data_mitigation)
#alpha_list, median_list_mitigation_test, mean_list_mitigation_test = fun_ben.cerate_data_alpha_plot(all_clusters_sets_dictionary,test_data_mitigation)


#alpha_list, median_list_prediction_traning, mean_list_prediction_traning = fun_ben.cerate_data_alpha_plot(all_clusters_sets_dictionary,traning_data_prediction)
#alpha_list, median_list_prediction_test, mean_list_prediction_test = fun_ben.cerate_data_alpha_plot(all_clusters_sets_dictionary,test_data_prediction)
#print("mitigation")
#print(median_list_mitigation_traning)
#print("prediction")
#print(median_list_prediction_traning)

max_value = max(comparison_dict.values())
max_key = max(comparison_dict,key=comparison_dict.get)

marginal_corrected_max = test_results[max_key[0]][max_key[1]]
marginal_ideal_max = ideal_benchmarks_dic[max_key[0]][max_key[1]]



print(max_value)
print(max_key)
print(marginal_corrected_max)
print(marginal_ideal_max)
print(all_clusters_sets_list)


