import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from copy import deepcopy
import adjustText as aT

import scienceplots
plt.style.use(['science','ieee'])

plt.rcParams["text.usetex"] = False

import os
GLOBAL_DIR = os.path.dirname(os.path.abspath(__file__))
NAMES_SELECTED = ["Ma 2.3 - AoA 8 - PIMPLE", "Ma 2.3 - AoA 16 - CENTRAL", "Ma 0.6 - AoA 8 - PIMPLE"]

def main ():

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    # open name files
    names = pd.read_csv(os.path.join(GLOBAL_DIR, "names.csv"), header=None).to_numpy()
    plot_names = []

    # find file name using the list of selected names
    for name in NAMES_SELECTED:
        for i in range(len(names)):
            if name == names[i][1]:
                FILE_PATH = os.path.join(GLOBAL_DIR, names[i][0] + ".csv")
                plot_names.append(FILE_PATH)
    
    df1 = pd.read_csv(plot_names[0], sep='\t')
    df2 = pd.read_csv(plot_names[1], sep='\t')
    df3 = pd.read_csv(plot_names[2], sep='\t')

    # select Cd, Cl, CmPitch rows from the dataframe
    df1.rename(columns=lambda x: x.replace(" ", ""), inplace=True)
    df1 = df1[['Cd', 'Cl', 'CmPitch']].to_numpy()

    df2.rename(columns=lambda x: x.replace(" ", ""), inplace=True)
    df2 = df2[['Cd', 'Cl', 'CmPitch']].to_numpy()

    df3.rename(columns=lambda x: x.replace(" ", ""), inplace=True)
    df3 = df3[['Cd', 'Cl', 'CmPitch']].to_numpy()

    df1_value = deepcopy(df1)
    df2_value = deepcopy(df2)
    df3_value = deepcopy(df3)

    # calculate relative error from the last value
    df1[:,0] = np.abs(df1[:,0] - df1[-1,0]) / df1[-1,0] * 100
    df1[:,1] = np.abs(df1[:,1] - df1[-1,1]) / df1[-1,1] * 100
    df1[:,2] = np.abs(df1[:,2] - df1[-1,2]) / df1[-1,2] * 100

    df2[:,0] = np.abs(df2[:,0] - df2[-1,0]) / df2[-1,0] * 100
    df2[:,1] = np.abs(df2[:,1] - df2[-1,1]) / df2[-1,1] * 100
    df2[:,2] = np.abs(df2[:,2] - df2[-1,2]) / df2[-1,2] * 100

    df3[:,0] = np.abs(df3[:,0] - df3[-1,0]) / df3[-1,0] * 100
    df3[:,1] = np.abs(df3[:,1] - df3[-1,1]) / df3[-1,1] * 100
    df3[:,2] = np.abs(df3[:,2] - df3[-1,2]) / df3[-1,2] * 100

    # delete last row
    df1 = np.delete(df1, -1, 0)
    df2 = np.delete(df2, -1, 0)
    df3 = np.delete(df3, -1, 0)

    # plot the relative error vs. iteration
    it = np.linspace(1, len(df1[:,0]), len(df1[:,0]))

    ax[0].plot(it, df1[:,0], label='CA', color='r', linestyle='-.', linewidth=1.5)
    ax[0].plot(it, df1[:,1], label='CN', color='b', linestyle='-.', linewidth=1.5)
    ax[0].plot(it, df1[:,2], label='CmPitch', color='g', linestyle='-.', linewidth=1.5)

    # scatter plot info
    ax[0].scatter(it, df1[:,0], color='r', marker='o', s=20)
    ax[0].scatter(it, df1[:,1], color='b', marker='o', s=20)
    ax[0].scatter(it, df1[:,2], color='g', marker='o', s=20)

    it = np.linspace(1, len(df2[:,0]), len(df2[:,0]))

    ax[1].plot(it, df2[:,0], label='CA', color='r', linestyle='-.', linewidth=1.5)
    ax[1].plot(it, df2[:,1], label='CN', color='b', linestyle='-.', linewidth=1.5)
    ax[1].plot(it, df2[:,2], label='CmPitch', color='g', linestyle='-.', linewidth=1.5)

    # scatter plot info
    ax[1].scatter(it, df2[:,0], color='r', marker='o', s=20)
    ax[1].scatter(it, df2[:,1], color='b', marker='o', s=20)
    ax[1].scatter(it, df2[:,2], color='g', marker='o', s=20)

    it = np.linspace(1, len(df3[:,0]), len(df3[:,0]))

    ax[2].plot(it, df3[:,0], label='CA', color='r', linestyle='-.', linewidth=1.5)
    ax[2].plot(it, df3[:,1], label='CN', color='b', linestyle='-.', linewidth=1.5)
    ax[2].plot(it, df3[:,2], label='CmPitch', color='g', linestyle='-.', linewidth=1.5)

    # scatter plot info
    ax[2].scatter(it, df3[:,0], color='r', marker='o', s=20)
    ax[2].scatter(it, df3[:,1], color='b', marker='o', s=20)
    ax[2].scatter(it, df3[:,2], color='g', marker='o', s=20)


    # Add value tag next to each scatter point using df1_value, df2_value, df3_value

    texts   = []
    texts.append(ax[0].text(0.95, 0.95, 'R5 Mesh:\nCA: {:.3f}\nCN: {:.3f}\nCmPitch: {:.3f}'.format(df1_value[-1,0], df1_value[-1,1], df1_value[-1,2]), horizontalalignment='right', verticalalignment='top', transform=ax[0].transAxes, fontsize=12))
    x = [0.95]
    y = [0.95]

    for i in range(len(df1_value[:,0])-1):

        texts.append(ax[0].text(it[i], df1[i,0], '{:.2f}'.format(df1_value[i,0]), c='r', fontsize=12))
        x.append(it[i])
        y.append(df1[i,0])

        texts.append(ax[0].text(it[i], df1[i,1], '{:.2f}'.format(df1_value[i,1]), c='b', fontsize=12))
        x.append(it[i])
        y.append(df1[i,1])

        texts.append(ax[0].text(it[i], df1[i,2], '{:.2f}'.format(df1_value[i,2]), c='g', fontsize=12))
        x.append(it[i])
        y.append(df1[i,2])
    
    aT.adjust_text(texts, x=x, y=y, ax=ax[0])

    texts   = []
    texts.append(ax[1].text(0.95, 0.95, 'R5 Mesh:\nCA: {:.3f}\nCN: {:.3f}\nCmPitch: {:.3f}'.format(df2_value[-1,0], df2_value[-1,1], df2_value[-1,2]), horizontalalignment='right', verticalalignment='top', transform=ax[1].transAxes, fontsize=12))
    x = [0.95]
    y = [0.95]

    for i in range(len(df2_value[:,0])-1):

        texts.append(ax[1].text(it[i], df2[i,0], '{:.2f}'.format(df2_value[i,0]), c='r', fontsize=12))
        x.append(it[i])
        y.append(df2[i,0])

        texts.append(ax[1].text(it[i], df2[i,1], '{:.2f}'.format(df2_value[i,1]), c='b', fontsize=12))
        x.append(it[i])
        y.append(df2[i,1])

        texts.append(ax[1].text(it[i], df2[i,2], '{:.2f}'.format(df2_value[i,2]), c='g', fontsize=12))
        x.append(it[i])
        y.append(df2[i,2])
    
    aT.adjust_text(texts, x=x, y=y, ax=ax[1])

    texts   = []
    texts.append(ax[2].text(0.95, 0.95, 'R5 Mesh:\nCA: {:.3f}\nCN: {:.3f}\nCmPitch: {:.3f}'.format(df3_value[-1,0], df3_value[-1,1], df3_value[-1,2]), horizontalalignment='right', verticalalignment='top', transform=ax[2].transAxes, fontsize=12))
    x = [0.95]
    y = [0.95]

    for i in range(len(df3_value[:,0])-1):

        texts.append(ax[2].text(it[i], df3[i,0], '{:.2f}'.format(df3_value[i,0]), c='r', fontsize=12))
        x.append(it[i])
        y.append(df3[i,0])

        texts.append(ax[2].text(it[i], df3[i,1], '{:.2f}'.format(df3_value[i,1]), c='b', fontsize=12))
        x.append(it[i])
        y.append(df3[i,1])

        texts.append(ax[2].text(it[i], df3[i,2], '{:.2f}'.format(df3_value[i,2]), c='g', fontsize=12))
        x.append(it[i])
        y.append(df3[i,2])
    
    aT.adjust_text(texts, x=x, y=y, ax=ax[2])

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
    ax[0].set_title(NAMES_SELECTED[0], fontsize=14)
    ax[1].set_title(NAMES_SELECTED[1], fontsize=14)
    ax[2].set_title(NAMES_SELECTED[2], fontsize=14)

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