import matplotlib.pyplot as plt
import pandas as pd

import scienceplots
plt.style.use(['science','ieee'])

plt.rcParams["text.usetex"] = False

import os
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

ZOOM = 30000
WINDOW = 20000


class Config:
    def __init__(self):
        self.MIN_TIME = 0
        self.MAX_TIME = 0

CONFIG = Config()
CONFIG2 = Config()

def main ():
    N = 13
    # read data from coefficients_2272.dat -> skip first N rows -> first read row is header
    data = pd.read_csv(WORKING_DIR + '/coefficient_2272.dat', sep='\t', skiprows=N).to_numpy()

    fig, ax = plt.subplots(3, 2, figsize=(15, 10), gridspec_kw={'width_ratios': [2, 1]})

    # subtract inital time to data
    data[:,0] -= data[0,0]
    # time in ms
    data[:,0] *= 1000

    # delete 90% of data
    data_re = data[::10]

    # plot data
    # ca -> Cd (drag coefficient)
    # cn -> Cl (lift coefficient)
    # cm -> CmPitch (moment coefficient)

    ca_re = data_re[:,1]
    cn_re = data_re[:,4]
    cm_re = data_re[:,7]

    # calculate mean and std
    ca_mean = ca_re.mean()
    cn_mean = cn_re.mean()
    cm_mean = cm_re.mean()

    # calculate std and mean within moving window of size WINDOW and save to array
    ca_std = pd.Series(ca_re).rolling(WINDOW).std()
    cn_std = pd.Series(cn_re).rolling(WINDOW).std()
    cm_std = pd.Series(cm_re).rolling(WINDOW).std()

    ca_mean = pd.Series(ca_re).rolling(WINDOW).mean()
    cn_mean = pd.Series(cn_re).rolling(WINDOW).mean()
    cm_mean = pd.Series(cm_re).rolling(WINDOW).mean()

    CONFIG.MIN_TIME = data_re[WINDOW,0]
    CONFIG.MAX_TIME = data_re[-1,0]

    # use dark gray color for data
    c_ = (0.2, 0.2, 0.2, 1)
    ax[0][0].plot(data_re[WINDOW:,0], ca_re[WINDOW:], color=c_, linestyle='--', label='data')
    ax[1][0].plot(data_re[WINDOW:,0], cn_re[WINDOW:], color=c_, linestyle='--', label='data')
    ax[2][0].plot(data_re[WINDOW:,0], cm_re[WINDOW:], color=c_, linestyle='--', label='data')

    # plot range and std
    # by coloring the area between mean+std and mean-std
    ax[0][0].fill_between(data_re[:,0], ca_mean+ca_std, ca_mean-ca_std, color='r', alpha=0.5, label='standard deviation')
    ax[1][0].fill_between(data_re[:,0], cn_mean+cn_std, cn_mean-cn_std, color='r', alpha=0.5, label='standard deviation')
    ax[2][0].fill_between(data_re[:,0], cm_mean+cm_std, cm_mean-cm_std, color='r', alpha=0.5, label='standard deviation')

    # plot mean
    ax[0][0].plot(data_re[:,0], ca_mean, color='r', linestyle='-', label='mean')
    ax[1][0].plot(data_re[:,0], cn_mean, color='r', linestyle='-', label='mean')
    ax[2][0].plot(data_re[:,0], cm_mean, color='r', linestyle='-', label='mean')

    # plot over all mean - thick line
    ax[0][0].axhline(y=ca_mean.mean(), color='g', linestyle='--', label='total mean', linewidth=3)
    ax[1][0].axhline(y=cn_mean.mean(), color='g', linestyle='--', label='total mean', linewidth=3)
    ax[2][0].axhline(y=cm_mean.mean(), color='g', linestyle='--', label='total mean', linewidth=3)

    # -----------------------------

    ca = data[:,1]
    cn = data[:,4]
    cm = data[:,7]

    CONFIG2.MIN_TIME = data[-ZOOM,0]
    CONFIG2.MAX_TIME = data[-1,0]

    ax[0][1].plot(data[-ZOOM:,0], ca[-ZOOM:], color=c_, linestyle='--', label='data')
    ax[1][1].plot(data[-ZOOM:,0], cn[-ZOOM:], color=c_, linestyle='--', label='data')
    ax[2][1].plot(data[-ZOOM:,0], cm[-ZOOM:], color=c_, linestyle='--', label='data')

    # style plot
    style_plot(fig, ax)

    fig.savefig(WORKING_DIR + "/{}.svg".format("transient"))


# -----------------------------

# style plot
def style_plot(fig, axs):

    # set labels
    axs[0][0].set_ylabel('CA', fontsize=12)
    axs[1][0].set_ylabel('CN', fontsize=12)
    axs[2][0].set_ylabel('CmPitch', fontsize=12)

    # set axis labels x
    axs[2][0].set_xlabel('Time [ms]', fontsize=12)
    axs[2][1].set_xlabel('Time [ms]', fontsize=12)

    # set legend
    axs[0][0].legend()

    # set y axis same from right to left based on maximum and minimum values of all plots
    max_ = max([axs[0][0].get_ylim()[1], axs[0][1].get_ylim()[1]])
    min_ = min([axs[0][0].get_ylim()[0], axs[0][1].get_ylim()[0]])
    axs[0][0].set_ylim([min_, max_])
    axs[0][1].set_ylim([min_, max_])

    max_ = max([axs[1][0].get_ylim()[1], axs[1][1].get_ylim()[1]])
    min_ = min([axs[1][0].get_ylim()[0], axs[1][1].get_ylim()[0]])
    axs[1][0].set_ylim([min_, max_])
    axs[1][1].set_ylim([min_, max_])

    max_ = max([axs[2][0].get_ylim()[1], axs[2][1].get_ylim()[1]])
    min_ = min([axs[2][0].get_ylim()[0], axs[2][1].get_ylim()[0]])
    axs[2][0].set_ylim([min_, max_])
    axs[2][1].set_ylim([min_, max_])

    # remove y axis numbers right plots
    axs[0][1].set_yticklabels([])
    axs[1][1].set_yticklabels([])
    axs[2][1].set_yticklabels([])

    # adjust x axis to ploted data range
    axs[0][0].set_xlim([CONFIG.MIN_TIME, CONFIG.MAX_TIME])
    axs[1][0].set_xlim([CONFIG.MIN_TIME, CONFIG.MAX_TIME])
    axs[2][0].set_xlim([CONFIG.MIN_TIME, CONFIG.MAX_TIME])

    axs[0][1].set_xlim([CONFIG2.MIN_TIME, CONFIG2.MAX_TIME])
    axs[1][1].set_xlim([CONFIG2.MIN_TIME, CONFIG2.MAX_TIME])
    axs[2][1].set_xlim([CONFIG2.MIN_TIME, CONFIG2.MAX_TIME])

    # get left and right plots closer together
    fig.subplots_adjust(wspace=0.02)

    # set grid
    axs[0][0].grid()
    axs[1][0].grid()
    axs[2][0].grid()

    axs[0][1].grid()
    axs[1][1].grid()
    axs[2][1].grid()

    # set sub titles
    axs[0][0].set_title("Entire Simulated Time - Range: {:.2f} - {:.2f} ms".format(CONFIG.MIN_TIME, CONFIG.MAX_TIME), fontsize=14)
    axs[0][1].set_title("Zoomed in - Range: {:.2f} - {:.2f} ms".format(CONFIG2.MIN_TIME, CONFIG2.MAX_TIME), fontsize=14)

    # make legend and axis labels font bigger
    for ax in axs.flat:
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend(fontsize=8)

    # add legend to plot above figure 
    handles, labels = axs[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=4, fontsize=12)

    # make legend invisible in all plots
    for ax in axs.flat:
        ax.legend().set_visible(False)

if __name__ == "__main__":
    main()