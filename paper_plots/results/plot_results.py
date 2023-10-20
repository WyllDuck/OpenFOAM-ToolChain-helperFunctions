import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline


import scienceplots
plt.style.use(['science','ieee'])

plt.rcParams["text.usetex"] = False

import os
GLOBAL_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
#           LOAD DATA
# -----------------------------

# get location file python
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

# simulation results - wind tunnel data too
df_res = pd.read_csv(WORKING_DIR + "/" + 'results.csv')

# wind tunnel data
df_tun_CA = pd.read_csv(WORKING_DIR + "/../../" + 'CA_coefficients.csv')
df_tun_Cm = pd.read_csv(WORKING_DIR + "/../../" + 'Cm_coefficients.csv')
df_tun_CN = pd.read_csv(WORKING_DIR + "/../../" + 'CN_coefficients.csv')

# get header .csv file with pandas - tunnel data
header_CA = df_tun_CA.columns.values.tolist()[1:]
header_CA = np.array([float(i.split('_')[0][1:]) for i in header_CA])

header_Cm = df_tun_Cm.columns.values.tolist()[1:]
header_Cm = np.array([float(i.split('_')[0][1:]) for i in header_Cm])

header_CN = df_tun_CN.columns.values.tolist()[1:]
header_CN = np.array([float(i.split('_')[0][1:]) for i in header_CN])

tun_CA = df_tun_CA.to_numpy()
tun_CA = tun_CA.astype(float)

tun_CN = df_tun_CN.to_numpy()
tun_CN = tun_CN.astype(float)

tun_Cm = df_tun_Cm.to_numpy()
tun_Cm = tun_Cm.astype(float)

ALPHA = 0.6


def main():

    # -----------------------------
    #           PLOT 1
    # -----------------------------

    # Plot the data
    fig1, axs1 = plt.subplots(1, 2, figsize=(10, 5))
    fig2, axs2 = plt.subplots(1, 3, figsize=(15, 5))

    solver = "PIMPLE"
    res_PIMPLE = df_res[df_res['SOLVER'] == solver].to_numpy()
    res_PIMPLE = res_PIMPLE[:,1:].astype(float)

    # group 1 colors (list of tuples) --> None element, orange, red
    # group 2 colors (list of tuples) --> None element, blue, dark-green
    # groups of colors: 

    color_group_1 = [(0, 0, 0), (1, 0.5, 0), (1, 0, 0)]
    color_group_2 = [(0, 0, 0), (0, 0, 1), (0, 0.5, 0)]

    for AoA in (0, 8, 16):
        c_ = color_group_1[AoA//8]

        data = np.array([i for i in res_PIMPLE if i[1] == AoA])
        
        # plot scatter with different shades of red for different AoA values
        if AoA == 0:
            axs2[0].scatter(data[:,0], data[:,2], label="PIMPLE", marker="o", color=(1, 0, 0))
            axs2[0].plot(data[:,0], data[:,2], color=(1, 0, 0, ALPHA), linestyle='dashed')
        elif AoA == 8:
            axs2[1].scatter(data[:,0], data[:,2], label="PIMPLE", marker="o", color=(1, 0, 0))
            axs2[1].plot(data[:,0], data[:,2], color=(1, 0, 0, ALPHA), linestyle='dashed')
        elif AoA == 16:
            axs2[2].scatter(data[:,0], data[:,2], label="PIMPLE", marker="o", color=(1, 0, 0))
            axs2[2].plot(data[:,0], data[:,2], color=(1, 0, 0, ALPHA), linestyle='dashed')
        else: 
            print("ERROR! AoA value not found")

        if AoA == 0:
            continue

        axs1[0].scatter(data[:,0], data[:,3], label="PIMPLE - AoA=" + str(AoA) + "°", marker="o", color=c_)
        axs1[1].scatter(data[:,0], data[:,4], label="PIMPLE - AoA=" + str(AoA) + "°", marker="o", color=c_)

        # add lines
        c_ = tuple(list(c_) + [ALPHA])
        axs1[0].plot(data[:,0], data[:,3], color=c_)
        axs1[1].plot(data[:,0], data[:,4], color=c_)

    solver = "CENTRAL"
    res_CENTRAL = df_res[df_res['SOLVER'] == solver].to_numpy()
    res_CENTRAL = res_CENTRAL[:,1:].astype(float)

    for AoA in (0, 8, 16):
        c_ = color_group_2[AoA//8]
        data = np.array([i for i in res_CENTRAL if i[1] == AoA])

        # plot scatter with different shades of red for different AoA values
        if AoA == 0:
            axs2[0].scatter(data[:,0], data[:,2], label="CENTRAL", marker="x", color=(0, 0, 1))
            axs2[0].plot(data[:,0], data[:,2], color=(0, 0, 1, ALPHA), linestyle='dotted')
        elif AoA == 8:
            axs2[1].scatter(data[:,0], data[:,2], label="CENTRAL", marker="x", color=(0, 0, 1))
            axs2[1].plot(data[:,0], data[:,2], color=(0, 0, 1, ALPHA), linestyle='dotted')
        elif AoA == 16:
            axs2[2].scatter(data[:,0], data[:,2], label="CENTRAL", marker="x", color=(0, 0, 1))
            axs2[2].plot(data[:,0], data[:,2], color=(0, 0, 1, ALPHA), linestyle='dotted')
        else: 
            print("ERROR! AoA value not found")

        if AoA == 0:
            continue

        # plot scatter with different shades of blue for different AoA values
        axs1[0].scatter(data[:,0], data[:,3], label="CENTRAL - AoA=" + str(AoA) + "°", marker="x", color=c_)
        axs1[1].scatter(data[:,0], data[:,4], label="CENTRAL - AoA=" + str(AoA) + "°", marker="x", color=c_)
        
        # add lines
        c_ = tuple(list(c_) + [ALPHA])
        axs1[0].plot(data[:,0], data[:,3], color=c_)
        axs1[1].plot(data[:,0], data[:,4], color=c_)

    plot_TUN_data(axs1,axs2)
    
    style_plot_axs1(fig1, axs1)
    style_plot_axs2(fig2, axs2)
    
    fig1.savefig(GLOBAL_DIR + "/{}.svg".format("side_moment_and_lift_coefficients"))
    fig2.savefig(GLOBAL_DIR + "/{}.svg".format("drag_coefficients")) 


# -----------------------------
#      HELPER FUNCTIONS
# -----------------------------

def style_plot_axs1(fig, axs):

    # set tittle all subplots
    fig.suptitle("Aerodynamic Lift and Pitching Moment Coefficients vs. Wind Tunnel Data", fontsize=16)

    # set axis labels
    axs[0].set_ylabel('CN', fontsize=12)
    axs[1].set_ylabel('CmPitch', fontsize=12)

    # set axis labels x
    axs[0].set_xlabel('Mach Number [-]', fontsize=12)
    axs[1].set_xlabel('Mach Number [-]', fontsize=12)

    # set legend
    axs[0].legend()

    # set grid
    axs[0].grid()
    axs[1].grid()

    # set all y-min to 0
    axs[0].set_ylim(bottom=0)
    axs[1].set_ylim(bottom=0)

    # make legend and axis labels font bigger
    for ax in axs.flat:
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend(fontsize=8)

    return


def style_plot_axs2(fig, axs):

    # set tittle all subplots
    fig.suptitle("Aerodynamic Drag Coefficients vs. Wind Tunnel Data", fontsize=16)

    # subtitle axis
    axs[0].set_title("AoA = 0°", fontsize=12)
    axs[1].set_title("AoA = 8°", fontsize=12)
    axs[2].set_title("AoA = 16°", fontsize=12)

    # set axis labels
    axs[0].set_ylabel('CA', fontsize=12)
    axs[1].set_ylabel('CA', fontsize=12)
    axs[2].set_ylabel('CA', fontsize=12)

    # set axis labels x
    axs[0].set_xlabel('Mach Number [-]', fontsize=12)
    axs[1].set_xlabel('Mach Number [-]', fontsize=12)
    axs[2].set_xlabel('Mach Number [-]', fontsize=12)

    # set legend - right corner
    axs[0].legend(loc='upper right')

    # set grid
    axs[0].grid()
    axs[1].grid()
    axs[2].grid()

    # set all y-max to 0.6
    axs[0].set_ylim(top=0.6)
    axs[1].set_ylim(top=0.6)
    axs[2].set_ylim(top=0.6)

    # set all y-min to 0.1
    axs[0].set_ylim(bottom=0.1)
    axs[1].set_ylim(bottom=0.1)
    axs[2].set_ylim(bottom=0.1)

    # make legend and axis labels font bigger
    for ax in axs.flat:
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend(fontsize=8)

    return


def plot_TUN_data (axs1, axs2):
    
    for AoA in (0, 8, 16):
        data_TUN_CA = tun_CA[np.where([tun_CA[:,0] == AoA]), :][1][0][1:]
        data_TUN_CN = tun_CN[np.where([tun_CN[:,0] == AoA]), :][1][0][1:]
        data_TUN_Cm = tun_Cm[np.where([tun_Cm[:,0] == AoA]), :][1][0][1:]

        # create 2 columns array with mach and coefficient
        data_TUN_CA = np.vstack([header_CA, data_TUN_CA]).T
        data_TUN_CN = np.vstack([header_CN, data_TUN_CN]).T
        data_TUN_Cm = np.vstack([header_Cm, data_TUN_Cm]).T

        data_TUN_CA = data_TUN_CA[np.argsort(data_TUN_CA[:,0])]
        data_TUN_CN = data_TUN_CN[np.argsort(data_TUN_CN[:,0])]
        data_TUN_Cm = data_TUN_Cm[np.argsort(data_TUN_Cm[:,0])]

        # use min and max headers to set xnew
        xnew = np.linspace(np.min(header_CA), np.max(header_CA), 300)

        # use 2nd order spline interpolation
        spl_CA = make_interp_spline(data_TUN_CA[:,0], data_TUN_CA[:,1], k=2)  # type: BSpline
        spl_CN = make_interp_spline(data_TUN_CN[:,0], data_TUN_CN[:,1], k=2)
        spl_Cm = make_interp_spline(data_TUN_Cm[:,0], data_TUN_Cm[:,1], k=2)

        if AoA == 0:
            axs2[0].plot(xnew, spl_CA(xnew), linestyle='dashed', label="Wind Tunnel Data")
            axs2[0].scatter(data_TUN_CA[:,0], data_TUN_CA[:,1], s=7, color=(0, 0, 0, 0.65))

        elif AoA == 8:
            axs2[1].plot(xnew, spl_CA(xnew), linestyle='dashed', label="Wind Tunnel Data")
            axs2[1].scatter(data_TUN_CA[:,0], data_TUN_CA[:,1], s=7, color=(0, 0, 0, 0.65))

        elif AoA == 16:
            axs2[2].plot(xnew, spl_CA(xnew), linestyle='dashed', label="Wind Tunnel Data")
            axs2[2].scatter(data_TUN_CA[:,0], data_TUN_CA[:,1], s=7, color=(0, 0, 0, 0.65))

        else:
            print("ERROR! AoA value not found")

        if AoA == 0:
            continue

        elif AoA == 8: 
            # plot dashed black line 
            axs1[0].plot(xnew, spl_CN(xnew), linestyle='dashed', color=(0, 0, 0), label="Wind Tunnel Data - AoA=" + str(AoA) + "°")
            axs1[1].plot(xnew, spl_Cm(xnew), linestyle='dashed', color=(0, 0, 0), label="Wind Tunnel Data - AoA=" + str(AoA) + "°")

        elif AoA == 16: 
            # plot doted dashed line 
            axs1[0].plot(xnew, spl_CN(xnew), linestyle='dotted', color=(0, 0, 0), label="Wind Tunnel Data - AoA=" + str(AoA) + "°")
            axs1[1].plot(xnew, spl_Cm(xnew), linestyle='dotted', color=(0, 0, 0), label="Wind Tunnel Data - AoA=" + str(AoA) + "°")

        else: 
            print("ERROR! AoA value not found")

        axs1[0].scatter(data_TUN_CN[:,0], data_TUN_CN[:,1], s=7, color=(0, 0, 0, 0.65))
        axs1[1].scatter(data_TUN_Cm[:,0], data_TUN_Cm[:,1], s=7, color=(0, 0, 0, 0.65))
               
    return


if __name__ == "__main__":
    main()