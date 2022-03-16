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

    # Consumed Power [W]
    P_bat = 0

    time    = 0             # start     [sec.]
    step    = 0.1           # dt        [sec.]
    
    # end     = bat.t_total   # end time  [sec.] - For Thermal Simulation
    end     = 3800          # end time  [sec.] - For Power Consumption Simulation
    
    t_data      = np.linspace(time, int(end-step), int((end-time)/step)) # time


    """ HEAT RELEATED SIMULATION """
    # Saved Values
    T_atm_data = np.zeros(int((end-time)/step))
    T_bat_data = np.zeros(int((end-time)/step))
    Q_dis_data = np.zeros(int((end-time)/step))
    W_dis_data = np.zeros(int((end-time)/step))

    Q_rad_data = np.zeros(int((end-time)/step))
    Q_cov_data = np.zeros(int((end-time)/step))

    """ POWER RELEATED SIMULATION """
    # Saved Values
    P_bat_data = np.zeros(int((end-time)/step))


    for i in range(len(t_data)):

        time = t_data[i]

        # START HERE
        """ HEAT RELEATED SIMULATION """
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

        """ POWER RELEATED SIMULATION """
        P_bat += W * step * (1/3600) # [Wh]

        # END HERE

        # Save Data
        """ HEAT RELEATED SIMULATION """
        T_atm_data[i] = T_atm
        T_bat_data[i] = T_bat
        Q_dis_data[i] = Q
        W_dis_data[i] = W

        Q_cov_data[i] = Q_conv
        Q_rad_data[i] = Q_rad

        """ POWER RELEATED SIMULATION """
        P_bat_data[i] = P_bat


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

    plt.plot(t_data, P_bat_data, label="Power Consumed [Wh]")
    plt.axhline(y=bat.cap_bat, color='red', linestyle='--', label="MAX Battery Capacity [Wh]")

    plt.legend(loc="lower right")
    plt.show()


if __name__ == "__main__":
    main()