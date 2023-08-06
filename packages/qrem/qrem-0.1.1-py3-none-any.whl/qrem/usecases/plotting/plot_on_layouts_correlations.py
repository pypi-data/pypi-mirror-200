"""
This is a script for plotting correlation coefficients on device layouts, for various datasets (simulator/IBM/Rigetti)
"""
import os, sys
from manim import *

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(FILE_PATH))

from qrem.visualisation.visualisation import ResultsForPlotting
from qrem.visualisation.device_constants import tutorial_simulator, washington, aspen_m_2
from read_data_for_plotting import *  # this is a simple script where plotted data is loaded

experiment_dictionary = {'used_qubits': [0, 1, 2, 3, 4],
                         'correlations': np.random.rand(5, 5) / 5}
experiment_instance = ResultsForPlotting(tutorial_simulator, experiment_dictionary)
clusters = ((1, 4), (2, 3, 5))
# experiment_instance.draw_clusters(list(clusters))
experiment_instance.draw_histogram()
experiment_instance.draw_heatmap()

# the data is loaded in script read_data_for_plotting:
correlations = QDT_errors_data_PLS_IBM260422['correlations_data']
metadata = QDT_errors_data_PLS_IBM260422['metadata']
date = '26_04_2022'

correlations = QDOT_correlations_ASPEN_M_2_2022_12_22['correlations_data']
metadata = QDOT_correlations_ASPEN_M_2_2022_12_22['metadata']
date = '22_12_2022'
device_name = 'aspen-m-2'

#Janek's version:
correlations = QDT_errors_data_POVMs_PLS_no_0_RIG010322['correlations_data']
metadata = QDT_errors_data_POVMs_PLS_no_0_RIG010322['metadata']
#Filip's version which is in overleaf:
# correlations = ASPEN_M_1_2022_03_01_diagonal_average_case['correlations_data']
# metadata = ASPEN_M_1_2022_03_01_diagonal_average_case['metadata']
#this is in overleaf now:
# used_qubits = []
# for key in ASPEN_M_1_2022_03_01_diagonal_average_case['qubits_mapping']:
#     used_qubits.append(ASPEN_M_1_2022_03_01_diagonal_average_case['qubits_mapping'][key])
#Filip's version downloaded from nextloud:
# correlations = ASPEN_M_1_2022_03_01_QDOT['correlations_table']
# used_qubits = ASPEN_M_1_2022_03_01_QDOT['true_qubits']
#
date = '01_03_2022'
device_name = 'aspen-m-1'


# correlations_ibm = QDT_errors_data_PLS_IBM281122['correlations_data']
# metadata_ibm = QDT_errors_data_PLS_IBM281122['metadata']
# date = '28_11_2022'

used_qubits = metadata['physical_qubits']

#map used qubits to non-Rigetti labelling:
used_qubits = [aspen_m_2['vertex_labels'].index(qubit) for qubit in used_qubits]
# experiment_dictionary = {'used_qubits': [0, 2, 3, 4],
#                          'correlations': np.random.rand(4, 4) / 5}

# # correlations_above_threshold
for key_distance_name in correlations:
    for key_classical_or_quantum in correlations[key_distance_name]:
        if key_distance_name == 'average_case' and key_classical_or_quantum == 'quantum':
            experiment_dictionary = {'used_qubits': used_qubits,
                                     'correlations': correlations[key_distance_name][key_classical_or_quantum]}
            experiment_instance = ResultsForPlotting(aspen_m_2, experiment_dictionary)
            threshold = 0.16
            experiment_instance.draw_on_layout(what_to_draw='correlations_above_threshold',
                                               correlations_threshold=threshold,
                                               file_name=device_name + '_' + date + '_' + key_distance_name + '_' +
                                                         key_classical_or_quantum + '_threshold_' + str(threshold * 100))
# # #
# experiment_dictionary = {'used_qubits': used_qubits,
#                          'correlations': correlations,
#                          }# 'correlations': correlations[key_distance_name][key_classical_or_quantum]}
# experiment_instance = ResultsForPlotting(aspen_m_2, experiment_dictionary)
# threshold = 0.04
# key_distance_name = 'average_case'
# key_classical_or_quantum = 'diagonal'
# experiment_instance.draw_on_layout(what_to_draw='correlations_above_threshold',
#                                    correlations_threshold=threshold,
#                                    file_name='QDOT_' + device_name + '_' + date + '_threshold_' + str(threshold * 100))
# # print attributes of experiment_instance:
# for key in experiment_instance.__dict__:
#     pass
#     # print(key, ':\n', experiment_instance.__dict__[key])
