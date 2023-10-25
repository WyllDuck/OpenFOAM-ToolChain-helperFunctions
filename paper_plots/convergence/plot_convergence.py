import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import scienceplots
plt.style.use(['science','ieee'])

plt.rcParams["text.usetex"] = False

import os
GLOBAL_DIR = os.path.dirname(os.path.abspath(__file__))


def main ():

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    df1 = pd.read_csv('{}/convergence_1.csv'.format(GLOBAL_DIR), sep='\t', header=None).to_numpy()
    df2 = pd.read_csv('{}/convergence_2.csv'.format(GLOBAL_DIR), sep='\t', header=None).to_numpy()
    df3 = pd.read_csv('{}/convergence_3.csv'.format(GLOBAL_DIR), sep='\t', header=None).to_numpy()

    # calculate relative error from the last value
    df1[:,0] = np.abs(df1[:,0] - df1[-1,0]) / df1[-1,0] * 100
    df1[:,1] = np.abs(df1[:,1] - df1[-1,1]) / df1[-1,1] * 100
    df1[:,2] = np.abs(df1[:,2] - df1[-1,2]) / df1[-1,2] * 100

    df2[:,0] = np.abs(df2[:,0] - df2[-1,0]) / df2[-1,0] * 100

    df3[:,0] = np.abs(df3[:,0] - df3[-1,0]) / df3[-1,0] * 100
    df3[:,1] = np.abs(df3[:,1] - df3[-1,1]) / df3[-1,1] * 100
    df3[:,2] = np.abs(df3[:,2] - df3[-1,2]) / df3[-1,2] * 100

    # delete last row
    df1 = np.delete(df1, -1, 0)
    df2 = np.delete(df2, -1, 0)
    df3 = np.delete(df3, -1, 0)

    # plot the relative error vs. iteration
    it = np.linspace(1, len(df1[:,0]), len(df1[:,0]))

    ax[0].plot(it, df1[:,0], label='CA', color='r', linestyle='-', linewidth=1.5)
    ax[0].plot(it, df1[:,1], label='CN', color='b', linestyle='-', linewidth=1.5)
    ax[0].plot(it, df1[:,2], label='CmPitch', color='g', linestyle='-', linewidth=1.5)

    # scatter plot info
    ax[0].scatter(it, df1[:,0], color='r', marker='o', s=20)
    ax[0].scatter(it, df1[:,1], color='b', marker='o', s=20)
    ax[0].scatter(it, df1[:,2], color='g', marker='o', s=20)

    it = np.linspace(1, len(df2[:,0]), len(df2[:,0]))

    ax[1].plot(it, df2[:,0], label='CA', color='r', linestyle='-', linewidth=1.5)

    # scatter plot info
    ax[1].scatter(it, df2[:,0], color='r', marker='o', s=20)

    it = np.linspace(1, len(df3[:,0]), len(df3[:,0]))

    ax[2].plot(it, df3[:,0], label='CA', color='r', linestyle='-', linewidth=1.5)
    ax[2].plot(it, df3[:,1], label='CN', color='b', linestyle='-', linewidth=1.5)
    ax[2].plot(it, df3[:,2], label='CmPitch', color='g', linestyle='-', linewidth=1.5)

    # scatter plot info
    ax[2].scatter(it, df3[:,0], color='r', marker='o', s=20)
    ax[2].scatter(it, df3[:,1], color='b', marker='o', s=20)
    ax[2].scatter(it, df3[:,2], color='g', marker='o', s=20)


    style_plot(fig, ax)

    fig.savefig('{}/convergence.svg'.format(GLOBAL_DIR))


def style_plot (fig, ax):

    # point yellow zone below 1% error
    ax[0].axhspan(0, 1, facecolor='y', alpha=0.5, label='Convergence Criteria')
    ax[1].axhspan(0, 1, facecolor='y', alpha=0.5, label='Convergence Criteria')
    ax[2].axhspan(0, 1, facecolor='y', alpha=0.5, label='Convergence Criteria')

    # add legend
    #ax[0].legend(loc='upper right', fontsize=12)
    #ax[1].legend(loc='upper right', fontsize=12)
    #ax[2].legend(loc='upper right', fontsize=12)

    # subplot titles
    ax[0].set_title('Ma 2.3 - AoA 8 deg - PIMPLE', fontsize=14)
    ax[1].set_title('Ma 1.5 - AoA 0 deg - PIMPLE', fontsize=14)
    ax[2].set_title('Ma 4.63 - AoA 16 deg - CENTRAL', fontsize=14)

    # change x axis names for R1, R2, R3, ... naming for the relative 1,2,3,4 numbers
    ax[0].set_xticks(np.array([1,2,3,4]), ["R1", "R2", "R3", "R4"])
    ax[1].set_xticks(np.array([1,2,3,4]), ["R1", "R2", "R3", "R4"])
    ax[2].set_xticks(np.array([1,2,3,4]), ["R1", "R2", "R3", "R4"])
    
    # make labels bigger
    ax[0].tick_params(axis='both', which='major', labelsize=12)
    ax[1].tick_params(axis='both', which='major', labelsize=12)
    ax[2].tick_params(axis='both', which='major', labelsize=12)

    # set grid
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()

    # set minimum and maximum y axis to 0 
    ax[0].set_ylim(bottom=0)
    ax[1].set_ylim(bottom=0)
    ax[2].set_ylim(bottom=0)

    # set x axis naming
    ax[0].set_xlabel('Mesh Refinement', fontsize=14)
    ax[1].set_xlabel('Mesh Refinement', fontsize=14)
    ax[2].set_xlabel('Mesh Refinement', fontsize=14)

    # set y axis naming
    ax[0].set_ylabel('Relative Error [\%]', fontsize=14)
    ax[1].set_ylabel('Relative Error [\%]', fontsize=14)
    ax[2].set_ylabel('Relative Error [\%]', fontsize=14)

    # add legend above figure
    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=12)

    # give more space between legend and plot
    fig.subplots_adjust(bottom=0.2)

    return



if __name__ == '__main__':
    main()