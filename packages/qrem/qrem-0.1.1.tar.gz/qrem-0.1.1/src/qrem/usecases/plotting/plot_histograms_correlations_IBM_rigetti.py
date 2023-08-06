"""
This is a script for plotting correlations histograms from QDOT data, both jointly for IBM and Rigetti and separately.
"""
import os, sys
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(FILE_PATH))

import matplotlib.pyplot as plt
import numpy as np
from read_data_for_plotting import *  # this is a simple script where plotted data is loaded
from qrem.visualisation.plotting_constants import color_map

plt.rc('text', usetex=True)
plt.rc('font', **{'family': 'serif',
                  'serif': ['Computer Modern'],
                  })

color_ibm_classical = color_map(0.00)
color_ibm_quantum = color_map(0.08)
color_rigetti_classical = color_map(0.40)
color_rigetti_quantum = color_map(0.95)

# the data is loaded in script read_data_for_plotting:
correlations_ibm = QDT_errors_data_PLS_IBM281122['correlations_data']
metadata_correlations_ibm = QDT_errors_data_PLS_IBM281122['metadata']

correlations_rigetti = QDOT_correlations_ASPEN_M_2_2022_12_22['correlations_data']
metadata_correlations_rigetti = QDOT_correlations_ASPEN_M_2_2022_12_22['metadata']

date_rigetti = '2022-12-22'
date_ibm = '2022-11-28'


def delete_diagonal_and_flatten(two_d_array):
    array_flattened = two_d_array.flatten()
    array_flattened = np.delete(array_flattened, range(0, len(array_flattened) + 1, len(two_d_array) + 1), 0)
    return array_flattened


# def plot_histogram(correlations_data_ibm, correlations_data_rigetti,
#                                 metadata_ibm=None, metadata_rigetti=None,
#                                 distance_name='worst_case',
#                                 if_cumulative=False):
def plot_histogram(correlations_data_ibm, correlations_data_rigetti,
                   metadata_ibm=None, metadata_rigetti=None,
                   distance_name='worst_case',
                   if_cumulative=False):
    correlations_ibm_classical = delete_diagonal_and_flatten(correlations_data_ibm[distance_name]['classical'])
    correlations_ibm_quantum = delete_diagonal_and_flatten(correlations_data_ibm[distance_name]['quantum'])
    correlations_rigetti_classical = delete_diagonal_and_flatten(correlations_data_rigetti[distance_name]['classical'])
    correlations_rigetti_quantum = delete_diagonal_and_flatten(correlations_data_rigetti[distance_name]['quantum'])
    if if_cumulative:
        type_of_histogram = 'step'
    else:
        type_of_histogram = 'bar'
    no_bins = 1000
    linewidths = 1.6
    opacity = 0.7
    if_stacked = False
    x_range_ibm = (0.0, np.amax(correlations_ibm_quantum))
    x_range_rigetti = (0.0, np.amax(correlations_rigetti_quantum))
    x_range_ibm_classical = (0.0, np.amax(correlations_ibm_classical))
    x_range_rigetti_classical = (0.0, np.amax(correlations_rigetti_classical))

    x_range = x_range_rigetti
    bins_sequence_ibm = [x / 10000 for x in
                         range(int(10000 * x_range_ibm[0]), int(10000 * (x_range_ibm[1] + 0.005)), 10)]
    bins_sequence_rigetti = [x / 10000 for x in
                             range(int(10000 * x_range_rigetti[0]), int(10000 * (x_range_rigetti[1] + 0.005)), 10)]
    bins_sequence_ibm_classical = [x / 10000 for x in
                                   range(int(10000 * x_range_ibm[0]), int(10000 * (x_range_ibm_classical[1] + 0.005)),
                                         10)]
    bins_sequence_rigetti_classical = [x / 10000 for x in range(int(10000 * x_range_ibm[0]),
                                                                int(10000 * (x_range_rigetti_classical[1] + 0.005)),
                                                                10)]

    x_left_cutoff = None  # 0.01
    x_right_cutoff = np.amax(
        [np.amax(correlations_rigetti_quantum), np.amax(correlations_rigetti_quantum)])  # ibm:0.25, rigetti:0.54
    y_top_cutoff = None  # joint: 750,from 1%: 50, for full: ibm: 9000, rigetti: 500;for over 1%: ibm: 60, rigetti: 150
    if_normalized = False

    fig, ax = plt.subplots(figsize=(8, 5))
    n2, bins2, patches2 = ax.hist(correlations_rigetti_quantum, bins_sequence_rigetti, density=if_normalized,
                                  histtype=type_of_histogram,
                                  cumulative=if_cumulative, label='Rigetti quantum', color=color_rigetti_quantum,
                                  linewidth=linewidths,
                                  stacked=if_stacked, alpha=opacity, range=x_range_rigetti)
    n3, bins3, patches3 = ax.hist(correlations_rigetti_classical, bins_sequence_rigetti_classical,
                                  density=if_normalized,
                                  histtype=type_of_histogram, cumulative=if_cumulative,
                                  label='Rigetti classical', color=color_rigetti_classical, linewidth=linewidths,
                                  linestyle='--', stacked=if_stacked, alpha=opacity, range=x_range_rigetti_classical)
    # n0, bins0, patches0 = ax.hist(correlations_ibm_quantum, bins_sequence_ibm, density=if_normalized,
    #                               histtype=type_of_histogram,
    #                               cumulative=if_cumulative, label='IBM quantum', color=color_ibm_quantum,
    #                               linewidth=linewidths,
    #                               stacked=if_stacked, alpha=opacity, range=x_range_ibm)
    # n1, bins1, patches1 = ax.hist(correlations_ibm_classical, bins_sequence_ibm_classical, density=if_normalized,
    #                               histtype=type_of_histogram,
    #                               cumulative=if_cumulative, label='IBM classical', color=color_ibm_classical,
    #                               linewidth=linewidths, linestyle='--', stacked=if_stacked, alpha=opacity,
    #                               range=x_range_ibm_classical)
    # # if not if_cumulative:
    #     n0 = n0 / 1000
    #     n1 = n1 / 1000
    #     n2 = n2/1000
    #     n3 = n3/1000
    #
    # normalizer0 = sum(n for n in n0)
    # normalizer1 = sum(n for n in n1)
    normalizer2 = sum(n for n in n2)
    normalizer3 = sum(n for n in n3)

    ax.legend(loc='lower right')
    ax.set_title(distance_name)
    ax.set_xlabel('Correlation coefficient')
    ax.set_xlim(x_left_cutoff, x_right_cutoff)

    if x_left_cutoff is not None:
        x_ticks = list(ax.get_xticks())
        x_ticks[0] = x_left_cutoff
        ax.set_xticks(x_ticks)
    if not if_cumulative:
        ax.set_ylim(0, y_top_cutoff)
        if if_normalized:
            y_vals = ax.get_yticks()
            ax.set_yticklabels(['{:1.2f}%'.format(x / 1000) for x in y_vals])

    if if_normalized:
        ax.set_ylabel('Fraction of all qubit pairs')
    else:
        ax.set_ylabel('Number of pairs')
    plt.savefig(
        'rigetti_' + date_rigetti + '_ibm_' + date_ibm + '_' + distance_name + '_cumulative_' + str(if_cumulative) +
        '_normalized_' + str(if_normalized) +
        '_opacity_' + str(opacity) + '_x_left_cutoff_' + str(x_left_cutoff) + '_y_cutoff_' + str(y_top_cutoff) +
        '.png', bbox_inches='tight', dpi=300)
    plt.show()


# metadata_dictionary = {}
# metadata_dictionary['ibm'] = metadata_correlations_ibm
# metadata_dictionary['rigetti'] = metadata_correlations_rigetti
#
# with open('metadata.pkl', 'wb') as file:
#     pickle.dump(metadata_dictionary, file, protocol=pickle.HIGHEST_PROTOCOL)
plot_histogram(correlations_ibm, correlations_rigetti)
