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

from qrem.noise_mitigation.probability_distributions.MarginalsCorrector import MarginalsCorrector
from qrem.noise_characterization.tomography_design.overlapping.DOTMarginalsAnalyzer import DOTMarginalsAnalyzer
from tqdm import tqdm


number_of_qubits=10
single_qubits =[(i,) for i in range(number_of_qubits) ]
pairs_of_qubits = [(i, j) for i in range(number_of_qubits) for j in range(i + 1, number_of_qubits)]

data_directory= 'C:\\CFT Chmura\\Theory of Quantum Computation\\QREM_Data\\ibm\\test_data\\'

with open(data_directory + "correction_data_now_deb"+'.pkl', 'rb') as filein:
    correction_dic = pickle.load(filein)

with open(data_directory + "benchmark_results_dic_deb"+'.pkl', 'rb') as filein:
    ben_result_dic = pickle.load(filein)

    

with open(data_directory + "benchmark_marginals_dic_deb"+'.pkl', 'rb') as filein:
    ben_marginals_dic = pickle.load(filein)


def correct_marginals_on_clusters_v2(marginals_dictionary,results_dictionary,correction_data,method_kwargs,mitigation_method,marginals_to_correct):
    noise_model_subsets=correction_data['subsets_to_correct']
    mitigated_marginals_dictionary ={}
    correction_indices_now= correction_data['correction_indices']
    for state_index, input_state in tqdm(enumerate(marginals_dictionary.keys())):
        marginals_dictionary_raw = marginals_dictionary[input_state]
        results_dictionary_raw = results_dictionary[input_state]
       


        #correction_data_now = {'subsets_to_correct': noise_model_subsets,
        #                               'correction_matrices_old': correction_matrices_dictionary,
        #                               'correction_matrices': correction_matrices_dictionary_new, 
        #                               'noise_matrices': noise_matrices_dictionary_model}
        
        missing_subsets=[]
        for needed_subset in marginals_to_correct:
            subset_for_correction = correction_indices_now[tuple(noise_model_subsets)][needed_subset]
            if subset_for_correction not in marginals_dictionary_raw.keys() and (subset_for_correction not in missing_subsets):
                missing_subsets.append(subset_for_correction)
        
        print(missing_subsets)

        if len(missing_subsets) > 0:
            marginals_analyzer = DOTMarginalsAnalyzer({input_state: results_dictionary_raw})
            marginals_analyzer.compute_all_marginals(missing_subsets,
                                                             show_progress_bar=False,
                                                             multiprocessing=False)

        marginals_dictionary_raw = {**marginals_dictionary_raw,
                                                **marginals_analyzer.marginals_dictionary[input_state]}
        
        print(marginals_dictionary_raw)

        marginals_corrector = MarginalsCorrector(
                    experimental_results_dictionary={input_state: results_dictionary_raw},
                    correction_data_dictionary=correction_data,
                    marginals_dictionary=marginals_dictionary_raw)
        
        marginals_dictionary_to_correct = {correction_indices_now[tuple(noise_model_subsets)][subset_to_correct]:
                                                       marginals_dictionary_raw[
                                                           correction_indices_now[tuple(noise_model_subsets)][subset_to_correct]]
                                                   for subset_to_correct in marginals_to_correct}
        
        
        print(marginals_dictionary_to_correct[(0,3)])


        marginals_corrector.correct_marginals(marginals_dictionary=marginals_dictionary_to_correct,
                                                      method_kwargs=method_kwargs,
                                                      method=mitigation_method
                                                              )
        print("corrected")
        print(marginals_corrector._corrected_marginals[(0,3)])
        print(marginals_corrector._corrected_marginals[(0,1,3)])
        
        #marginals_coarse_grained_corrected = \
        #            marginals_corrector.compute_marginals_of_marginals(
        #                noise_model_subsets,
        #                corrected=True)

        marginals_coarse_grained_corrected = marginals_corrector.compute_marginals_of_marginals(
                        noise_model_subsets,
                        corrected=True)
        
        print(marginals_coarse_grained_corrected[(0,3)])

        
        mitigated_marginals_dictionary[input_state] = marginals_coarse_grained_corrected


    return mitigated_marginals_dictionary

mitigation_method = 'lambda_inverse'
method_kwargs = {'ensure_physicality': True}
mg_to_corr= single_qubits+pairs_of_qubits
correct_marginals_on_clusters_v2(ben_marginals_dic,ben_result_dic,correction_dic,method_kwargs,mitigation_method,mg_to_corr)

name_string = '2023-03-13 q10'

with open(data_directory +"DDOT_clusters_workflow_" + name_string +'.pkl', 'rb') as filein:
    clusters_dictionary = pickle.load(filein)

with open(data_directory + 'DDOT_noisy_simulation_results_' + name_string +'.pkl', 'rb') as filein:
    noisy_results_dictionary = pickle.load(filein)

    

with open(data_directory +'DDOT_marginals_workflow_' + name_string +'.pkl', 'rb') as filein:
    marginals_dictionary = pickle.load(filein)


correction_matrices, correction_indices,mitigation_data_dictionary = fdt.get_multiple_mitigation_strategies_clusters_for_pairs_of_qubits(
    pairs_of_qubits=pairs_of_qubits,
    clusters_sets=clusters_dictionary['all_clusters_sets_dictionary'],
    dictionary_results=noisy_results_dictionary,
    noise_matrices_dictionary=clusters_dictionary['noise_matrices_dictionary'],
    show_progress_bar=True)

print('ok')