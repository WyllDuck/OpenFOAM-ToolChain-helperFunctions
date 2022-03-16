# Imports
import numpy as np
import matplotlib.pyplot as plt

# Others
from atmosphere import Cylinder 
from rocket import Rocket
from battery import Battery


""" MAIN """
def main ():

    # Simulation Objects
    bat = Battery()
    rck = Rocket()
    atm = Cylinder()

    # Temperature Battery on Pre-launch
    T_bat   = 20 + 273.15   # [K]

    # Temperature Environment Radiation
    T_env   = 20 + 273.15   # [K]

    time    = 0             # start     [sec.]
    step    = 0.1           # dt        [sec.]
    end     = bat.t_total   # end time  [sec.]
    i       = 0

    # Saved Values
    T_atm_data  = np.zeros(int((end-time)/step))
    T_bat_data  = np.zeros(int((end-time)/step))
    Q_dis_data  = np.zeros(int((end-time)/step))
    W_dis_data  = np.zeros(int((end-time)/step))

    Q_rad_data  = np.zeros(int((end-time)/step))
    Q_cov_data  = np.zeros(int((end-time)/step))

    t_data      = np.linspace(time, int(end-step), int((end-time)/step)) # time

    while time < end: #-step

        # START HERE
        alt     = rck.get_altitude(time)
        T_atm   = atm.get_T(alt)
        Q, W    = bat.get_Q_dis(time) # dissipated heat, and power consumption

        h_atm   = atm.get_h(alt, 40+273.15) # no data for lower temperatures
        Q_conv  = h_atm * (T_bat - T_atm) # unit surface
        
        #Q_rad   = 0 # NOTE: We consider the environment (inside the rocket) at the same temperature. No radiation heat transfer 
        T_env = T_atm # option 1, else const. T_env
        Q_rad   = 5.67e-8*(pow(T_bat, 4) - pow(T_env, 4)) # NOTE: This is the worst case scenario

        dTdt = bat.get_dT(time, Q_conv, Q_rad)
        T_bat = T_bat + dTdt * step
        # END HERE

        # Save Data
        T_atm_data[i] = T_atm
        T_bat_data[i] = T_bat
        Q_dis_data[i] = Q
        W_dis_data[i] = W

        Q_cov_data[i] = Q_conv
        Q_rad_data[i] = Q_rad

        time    += step # next step
        i       += 1


    """ PLOT """
    plt.plot(t_data, T_atm_data - 273.15, label="Temperature Atmosphere [ºC]")
    plt.plot(t_data, T_bat_data - 273.15, label="Temperature Battery [ºC]")
    plt.plot(t_data, Q_dis_data, label="Q dissipated [J/sec]")
    plt.plot(t_data, W_dis_data, label="W Battery [J/sec]")

    plt.legend(loc="upper right")
    plt.show()

    plt.plot(t_data, Q_rad_data, label="Q radiation [J/sec]")
    plt.plot(t_data, Q_cov_data, label="Q convection [J/sec]")

    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    main()