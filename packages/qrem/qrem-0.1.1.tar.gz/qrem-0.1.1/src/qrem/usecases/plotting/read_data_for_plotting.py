"""
This is a script for loading data used for plotting
"""
import pickle
import os

cwd = os.getcwd()

# coherence:
# data_path = f"{cwd}\\data\\ibm\\coherence_indicator_IBM260422.pkl"
# with open(data_path, "rb") as input_file:
#     coherence_indicator_IBM260422 = pickle.load(input_file)

# # correlations:
data_path = f"{cwd}\\data\\ibm\\QDT_errors_data_PLS_IBM260422.pkl"
with open(data_path, "rb") as input_file:
    QDT_errors_data_PLS_IBM260422 = pickle.load(input_file)

# # correlations:
data_path = f"{cwd}\\data\\ibm\\QDOT_correlations_PLS_IBM_WAS_281122.pkl"
with open(data_path, "rb") as input_file:
    QDT_errors_data_PLS_IBM281122 = pickle.load(input_file)

# # clusters:
# data_path = f"{cwd}\\data\\ibm\\Reconstructed_noise_model_PLS_worstcase_classical_IBM260422.pkl"
# with open(data_path, "rb") as input_file:
#     Reconstructed_noise_model_PLS_worstcase_classical_IBM260422 = pickle.load(input_file)

# # marginals:
# data_path = f"{cwd}\\data\\ibm\\QDT_21_marginals_IBM260422.pkl"
# with open(data_path, "rb") as input_file:
#     QDT_21_marginals_IBM260422 = pickle.load(input_file)

# clusters:
# data_path = f"{cwd}\\data\\rigetti\\noise_models\\clusters\\batched_noise_matrices-PLS-worst_case-classical_no_0.pkl"
# with open(data_path, "rb") as input_file:
#     batched_noise_matrices_PLS_worst_case_classical_no_0 = pickle.load(input_file)
#
# for idx, key in enumerate(batched_noise_matrices_PLS_worst_case_classical_no_0['all_clusters_sets_dictionary']):
#     if idx == 22:
#         last_cluster_list = key

# 2-qubit reduced_POVMs:
# data_path = f"{cwd}\\data\\rigetti\\QDT_21_reduced_POVMS_PLS_0_RIG01322.pkl"
# with open(data_path, "rb") as input_file:
#     QDT_21_reduced_POVMS_PLS_0_RIG01322 = pickle.load(input_file)

# # correlations from Janek:
data_path = f"{cwd}\\data\\rigetti\\QDT_errors_data_POVMs-PLS_no_0_RIG010322.pkl"
with open(data_path, "rb") as input_file:
    QDT_errors_data_POVMs_PLS_no_0_RIG010322 = pickle.load(input_file)

# # correlations:
data_path = f"{cwd}\\data\\rigetti\\QDOT_correlations_ASPEN-M-2_2022-12-22.pkl"
with open(data_path, "rb") as input_file:
    QDOT_correlations_ASPEN_M_2_2022_12_22 = pickle.load(input_file)

# # correlations from FIlip from slack, currently (08.01.2023) plotted in overleaf:
data_path = f"{cwd}\\data\\rigetti\\ASPEN-M-1_2022-03-01_diagonal_average-case-saved2022-06-17.pkl"
with open(data_path, "rb") as input_file:
    ASPEN_M_1_2022_03_01_diagonal_average_case = pickle.load(input_file)

# something of Filip's downloaded from nextloud DDOT:
data_path = f"{cwd}\\data\\rigetti\\number_of_qubits_55\\noise_analysis_DDOT.pkl"
with open(data_path, "rb") as input_file:
    ASPEN_M_1_2022_03_01_DDOT = pickle.load(input_file)

# something of Filip's downloaded from nextloud QDOT:
data_path = f"{cwd}\\data\\rigetti\\number_of_qubits_55\\noise_analysis_QDOT.pkl"
with open(data_path, "rb") as input_file:
    ASPEN_M_1_2022_03_01_QDOT = pickle.load(input_file)