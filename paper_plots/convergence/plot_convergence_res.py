import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import scienceplots
plt.style.use(['science','ieee'])
plt.rcParams["text.usetex"] = False

import os
GLOBAL_DIR = os.path.dirname(os.path.abspath(__file__))
NAMES_SELECTED = ["Ma 2.3 - AoA 8 - PIMPLE", "Ma 2.3 - AoA 16 - CENTRAL", "Ma 0.6 - AoA 8 - PIMPLE"]

def main ():

    # open name files
    names = pd.read_csv(os.path.join(GLOBAL_DIR, "names.csv"), header=None).to_numpy()
    plot_names = []

    # find file name using the list of selected names
    for name in NAMES_SELECTED:
        for i in range(len(names)):
            if name == names[i][1]:
                FILE_PATH = os.path.join(GLOBAL_DIR, names[i][0] + "_res.csv")
                plot_names.append(FILE_PATH)

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    RET_residuals1, initial_headers1, number_iterations1 = read_residuals(plot_names[0])
    RET_residuals2, initial_headers2, number_iterations2 = read_residuals(plot_names[1])
    RET_residuals3, initial_headers3, number_iterations3 = read_residuals(plot_names[2])

    if not RET_residuals1 is None:
        plot_ax(ax[0], RET_residuals1, initial_headers1, number_iterations1)
    
    if not RET_residuals2 is None:
        plot_ax(ax[1], RET_residuals2, initial_headers2, number_iterations2)
    
    if not RET_residuals3 is None:
        plot_ax(ax[2], RET_residuals3, initial_headers3, number_iterations3)

    style_plot(fig, ax)

    # save figure
    plt.savefig(os.path.join(GLOBAL_DIR, 'convergence_res.svg'))


def plot_ax (axs, RET_residuals, initial_headers, number_iterations):

    # y_axis should be log scale
    axs.set_yscale('log')

    # plot the residuals vs. mesh resolution
    for i in range(len(RET_residuals)):
        axs.plot([1,2,3,4,5], RET_residuals[i], label=initial_headers[i])

        # x labels with name of mesh (R1, R2, R3, R4, R5) and number of iterations
        axs.set_xticks([1,2,3,4,5])
        axs.set_xticklabels(['R1\n(it. {})'.format(number_iterations[0]), 'R2\n(it. {})'.format(number_iterations[1]), 'R3\n(it. {})'.format(number_iterations[2]), 'R4\n(it. {})'.format(number_iterations[3]), 'R5\n(it. {})'.format(number_iterations[4])])

    return


# set line with given label to have given style based on dictionary input
def set_line_style (ax, label, style_dict):
    for line in ax.lines:
        if line.get_label() == label:
            line.set_linestyle(style_dict[label][0])
            line.set_color(style_dict[label][1])
            line.set_marker(style_dict[label][2])
            line.set_markersize(style_dict[label][3])
            line.set_markerfacecolor(style_dict[label][4])
            line.set_markeredgecolor(style_dict[label][5])
            

def style_plot (fig, ax):

    # create dictionary with line styles
    style_dict = {
        'e': ['-', 'r', 'o', 5, 'r', 'r'],
        'p': ['-', 'b', 'o', 5, 'b', 'b'],
        'omega': ['-', 'g', 'o', 5, 'g', 'g'],
        'k': ['-', 'm', 'o', 5, 'm', 'm'],
        'Ux': ['-', 'c', 'o', 5, 'c', 'c'],
        'Uy': ['-', 'y', 'o', 5, 'y', 'y'],
        'Uz': ['-', 'k', 'o', 5, 'k', 'k'],
    }

    # set line style for each subplot
    for i in range(len(ax)):
        for line in ax[i].lines:
            set_line_style(ax[i], line.get_label(), style_dict)
    
    # subplot titles
    ax[0].set_title(NAMES_SELECTED[0], fontsize=14)
    ax[1].set_title(NAMES_SELECTED[1], fontsize=14)
    ax[2].set_title(NAMES_SELECTED[2], fontsize=14)

    # make labels bigger
    ax[0].tick_params(axis='both', which='major', labelsize=12)
    ax[1].tick_params(axis='both', which='major', labelsize=12)
    ax[2].tick_params(axis='both', which='major', labelsize=12)

    # set grid
    ax[0].grid()
    ax[1].grid()
    ax[2].grid()

    # set x axis naming
    ax[0].set_xlabel('Mesh Refinement', fontsize=14)
    ax[1].set_xlabel('Mesh Refinement', fontsize=14)
    ax[2].set_xlabel('Mesh Refinement', fontsize=14)

    # set y axis naming
    ax[0].set_ylabel('Final Iteration Residuals', fontsize=14)
    ax[1].set_ylabel('Final Iteration Residuals', fontsize=14)
    ax[2].set_ylabel('Final Iteration Residuals', fontsize=14)

    # add legend above figure
    handles, labels = ax[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=12)

    # give more space between legend and plot
    fig.subplots_adjust(bottom=0.25)

    # same y axis scale for all subplots
    ax[0].set_ylim(bottom=1e-12, top=1e-3)
    ax[1].set_ylim(bottom=1e-12, top=1e-3)
    ax[2].set_ylim(bottom=1e-12, top=1e-3)

    return


# read residuals data
# returns: residuals
def read_residuals (FILE_PATH):
    try:
        residuals = pd.read_csv(FILE_PATH, sep='\t')
    except:
        print(f'Error reading residuals file {FILE_PATH}')
        return None, None, None
        
    residuals.rename(columns=lambda x: x.replace(" ", ""), inplace=True)
    
    # find all headers with '_initial' written in them - pandas
    initial_headers = []
    for header in residuals.columns:
        if '_initial' in header:
            
            # remove '_initial' from header
            header = header.replace('_initial', '')
            
            # if header + '_solver' exists, then 
            if header + '_solver' in residuals.columns:
                
                # if is has a row entry equal to 'diagonal', then ignore
                if residuals[header + '_solver'][0] == 'diagonal':
                    print(f'ignoring {header} because it is diagonal')
                    continue
            
            else: 
                
                # if all values in column header+'_initial' are null, then ignore
                if sum(residuals[header + '_initial']) == 0:
                    print(f'ignoring {header} because all values are null')
                    continue
            
            initial_headers.append(header)

    # loop thorugh every selected header and return last value
    RET_residuals = []
    for header in initial_headers:
        RET_residuals.append(residuals[header + "_initial"])

    # get number of iterations
    number_iterations = residuals["#Time"]

    return RET_residuals, initial_headers, number_iterations


if __name__ == '__main__':
    main()