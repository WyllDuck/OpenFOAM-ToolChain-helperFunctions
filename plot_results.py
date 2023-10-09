import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

import scienceplots
plt.style.use(['science','ieee'])

plt.rcParams["text.usetex"] = False

# -----------------------------
#           LOAD DATA
# -----------------------------

# get location file python
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

# simulation results - wind tunnel data too
df_res = pd.read_csv(WORKING_DIR + "/" + 'results.csv')

# wind tunnel data
df_tun_CA = pd.read_csv(WORKING_DIR + "/" + 'CA_coefficients.csv')
df_tun_Cm = pd.read_csv(WORKING_DIR + "/" + 'Cm_coefficients.csv')
df_tun_CN = pd.read_csv(WORKING_DIR + "/" + 'CN_coefficients.csv')

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


def main():

    # -----------------------------
    #           PLOT 1
    # -----------------------------

    # Plot the data
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    solver = "PIMPLE"
    res_PIMPLE = df_res[df_res['SOLVER'] == solver].to_numpy()
    res_PIMPLE = res_PIMPLE[:,1:].astype(float)

    for AoA in (0, 8, 16):
        data = np.array([i for i in res_PIMPLE if i[1] == AoA])

        axs[0].scatter(data[:,0], data[:,2], label="AoA=" + str(AoA) + "°", marker="x")
        axs[1].scatter(data[:,0], data[:,3], label="AoA=" + str(AoA) + "°", marker="x")
        axs[2].scatter(data[:,0], data[:,4], label="AoA=" + str(AoA) + "°", marker="x")

    plt.title("Aerodynamic Coefficients rhoPimpleFoam vs. wind tunnel data")
    plot_TUN_data2(axs)
    style_plot(axs)

    #plt.show()
    plt.savefig("PIMPLE.svg")

    # -----------------------------
    #           PLOT 2
    # -----------------------------

    # Plot the data
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    solver = "CENTRAL"
    res_CENTRAL = df_res[df_res['SOLVER'] == solver].to_numpy()
    res_CENTRAL = res_CENTRAL[:,1:].astype(float)

    for AoA in (0, 8, 16):
        data_SIM = np.array([i for i in res_CENTRAL if i[1] == AoA])

        axs[0].scatter(data_SIM[:,0], data_SIM[:,2], label="AoA=" + str(AoA) + "°", marker="x")
        axs[1].scatter(data_SIM[:,0], data_SIM[:,3], label="AoA=" + str(AoA) + "°", marker="x")
        axs[2].scatter(data_SIM[:,0], data_SIM[:,4], label="AoA=" + str(AoA) + "°", marker="x")

    plt.title("Aerodynamic Coefficients rhoCentralFoam vs. wind tunnel data")
    plot_TUN_data2(axs)
    style_plot(axs)

    #plt.show()
    plt.savefig("CENTRAL.svg")


# -----------------------------
#      HELPER FUNCTIONS
# -----------------------------

def style_plot(axs):

    # set axis labels
    axs[0].set_ylabel('Cd')
    axs[1].set_ylabel('Cl')
    axs[2].set_ylabel('CmPitch')

    # set axis labels x
    axs[0].set_xlabel('Mach Number [-]')
    axs[1].set_xlabel('Mach Number [-]')
    axs[2].set_xlabel('Mach Number [-]')

    # set legend
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()

    # set grid
    axs[0].grid()
    axs[1].grid()
    axs[2].grid()

    return


# use data from excel file
def plot_TUN_data2 (axs):

    solver = "PIMPLE"
    res_PIMPLE = df_res[df_res['SOLVER'] == solver].to_numpy()
    res_PIMPLE = res_PIMPLE[:,1:].astype(float)
    
    for AoA in (0, 8, 16):
        data = np.array([i for i in res_PIMPLE if i[1] == AoA])

        axs[0].plot(data[:,0], data[:,5])
        axs[1].plot(data[:,0], data[:,6])
        axs[2].plot(data[:,0], data[:,7])

    return

def plot_TUN_data (axs):
    
    for AoA in (0, 8, 16):
        data_TUN_CA = tun_CA[np.where([tun_CA[:,0] == AoA]), :][1]
        data_TUN_CN = tun_CN[np.where([tun_CN[:,0] == AoA]), :][1]
        data_TUN_Cm = tun_Cm[np.where([tun_Cm[:,0] == AoA]), :][1]

        # flatten array
        data_TUN_CA = data_TUN_CA.flatten()
        data_TUN_CN = data_TUN_CN.flatten()
        data_TUN_Cm = data_TUN_Cm.flatten()

        print(data_TUN_CA)
        print(data_TUN_CN)
        print(data_TUN_Cm)

        axs[0].plot(header_CA, data_TUN_CA[1:])
        axs[1].plot(header_CN, data_TUN_CN[1:])
        axs[2].plot(header_Cm, data_TUN_Cm[1:])

    return



if __name__ == "__main__":
    main()