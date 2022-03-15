import numpy as np
import matplotlib.pyplot as plt


# Battery
class Battery (object):

    def __init__ (self):

        # Configuration Battery
        self.s = 7      # series
        self.p = 2      # parallel

        # Cell Parameters
        self.R_int       = 80e-3             # Internal Resistance Cell [ohms]
        self.V_cell      = (4.2 + 2.75) / 2  # Mean Cell Voltage [V]

        # Mission Stages
        self.t_stages    = [0, 88, 26.5, 7, 23.5, 3, 767, 3, 72]    # duration of each stage [sec.]
        self.t_total     = sum(self.t_stages)                       # total duration of mission [sec.]

        self.w_stages    = [120, 48, 96, 48, 0, 20, 0, 20, 48]      # consumption in each stage [W]
        self.w_static    = 27.21                                    # Static Power Consumption [W]

        # Dimension Battery
        self.a = 8.5e-2 # side a [m]
        self.b = 8.5e-2 # side b [m]
        self.c = 6.5e-2 # side c [m]

        # Surface and Volume
        self.A = self.a * self.b * 2 + self.a * self.c * 2 # + self.b * self.c * 2 # [m^2] b and c can be considered adiabatic
        self.V = self.a * self.b * self.c # [m^3]

        # Heat Transfer and Thermal Diffusivity
        self.k = 237            # [W/(m*K)] aluminium
        self.alpha = 97e-6      # [m^2/s] aluminium


    # Heat Dissipated [W]
    # input: time [sec.] | output: Q [W]
    def get_Q_dis (self, t):

        index = self.find_stage(t)

        W = self.w_stages[index] + self.w_static    # power demand of the system
        I = W / (self.V_cell * self.s)              # intensity demand based on battery voltage

        # Heat Dissipated [W]
        Q_cell = pow((I / self.p), 2) * self.R_int
        Q_bat = self.s * self.p * Q_cell

        return Q_bat, W


    # Temperature Differential
    def get_dT (self, time, Q_conv, Q_rad):
        
        Q_dis, W    = self.get_Q_dis(time)
        Q_tot       = Q_conv + Q_rad - Q_dis / self.V
        dTdt        = (- Q_tot / self.k * self.A) * self.alpha / self.V

        return dTdt



    """ AUXILIARY FUNCTIONS """
    # Find Current Stage
    def find_stage (self, time):
        sum_ = 0
        for i in range(len(self.t_stages)):
            sum_ += self.t_stages[i]
            if sum_ > time:
                return i
        return len(self.t_stages) - 1


if __name__ == "__main__":
    
    bat = Battery()
    
    # Saved Values
    Q_data = []
    W_data = []
    t_data = []

    time    = 0
    dt      = 0.01 # step

    while time < bat.t_total:

        Q, W = bat.get_Q_dis(time)

        # Save Data
        Q_data.append(Q)
        W_data.append(W)
        t_data.append(time)

        time += dt # next step

    plt.plot(t_data, Q_data)
    plt.plot(t_data, W_data)
    plt.show()