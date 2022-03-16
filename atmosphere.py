import numpy as np
import matplotlib.pyplot as plt
from math import exp
from scipy import interpolate


# ICAO - International Standard Atmosphere
class Atmosphere (object):

    def __init__ (self):

        self.T0 = 288.15    # [K] => 15 [ºC]
        self.p0 = 1.013e5   # [N/m^2] => 1 [atm]
        self.d0 = 1.225     # [kg/m^3]

        self.Rsp = 287      # dry air R specific number [m^2/s^2/K]

        # source: https://en.wikipedia.org/wiki/International_Standard_Atmosphere
        self.id  = ["TRP_S", "TRP_P", "STR_S1", "STR_S2", "STR_P", "MS_S1", "MS_S2", "MS_P"]
        self.alt = [0, 11019, 20063, 32162, 47350, 51413, 71802, 86000] # position where layer starts [m]

        # NOTE: positive means temperature decreases with altitude
        self.dT  = [6.5e-3, 0.0e-3, -1.0e-3, -2.8e-3, 0.0e-3, 2.8e-3, 2.0e-3, 0.0e-3] # [K/m] 


    # Temparature [K]
    # Reviewed: CORRECT! (Félix Martí Valverde - 14/03/2022)
    def get_T (self, h):

        index = self.find_index(h)

        T = self.T0

        for i in range(index):
            T -= (self.alt[i+1] - self.alt[i]) * self.dT[i]        
        T -= (h - self.alt[index]) * self.dT[index]
                
        return T

        
    # Pressure
    # source: https://www.grc.nasa.gov/WWW/K-12/airplane/atmosmet.html
    # Reviewed: CORRECT! (Félix Martí Valverde - 14/03/2022)
    def get_p (self, h):

        T = self.get_T(h)

        if h <= 11000:
            return (101.29 * pow((T/self.T0), 5.256)) * 1e3

        elif h <= 25000:
            return (22.65 * exp(1.73 - 0.000157 * h)) * 1e3

        elif h <= 50000:
            return (2.488 * pow(T/216.6, -11.388)) * 1e3

        elif h <= 90000:
            return self.p0 * 0.1/100 # 0.1 % of initial atmosphere

        else:
            return self.p0 * 0.0001/100 # 0.0001 % of initial atmosphere


    # Density
    # formula: P/d^n = const
    def get_density (self, h):

        n = self.get_n(h)
        p = self.get_p(h)

        return pow(pow(self.d0, n) / self.p0 * p, 1/n)


    """ AUXILIARY FUNCTIONS """
    # Input: Height (h)
    # Returns: Index Layer (i)
    def find_index (self, h):

        for i in range(len(self.alt)):
            if self.alt[i] > h:
                if i == 0:  return 0
                else:       return i - 1
        
        # failed return highest layer
        return len(self.alt) - 1


    def get_n (self, h):

        index = self.find_index(h)
        return pow(1 + self.Rsp / 9.81 * -self.dT[index], -1)


class Cylinder (Atmosphere):

    def __init__(self):
        super().__init__()

        # Heat Transfer Table
        self.conv_h =  [[0.86, 1.78, 4.35,  7.02,  9.01,  9.73, 10.06, 11.17, 11.93],
                        [1.70, 3.12, 6.16,  9.27, 11.90, 12.84, 13.72, 14.87, 16.36],
                        [2.56, 4.14, 7.40, 10.54, 13.36, 14.47, 15.61, 16.72, 17.98],
                        [3.16, 4.74, 7.99, 11.44, 14.17, 15.62, 16.37, 17.80, 18.85],
                        [3.47, 5.11, 8.44, 11.70, 14.67, 15.83, 16.59, 18.32, 19.35],
                        [3.60, 5.30, 8.56, 12.01, 14.95, 16.14, 16.92, 18.47, 19.64],
                        [3.51, 5.24, 8.52, 11.99, 15.06, 16.16, 17.02, 18.48, 19.80]]

        self.conv_h = np.array(self.conv_h)

        self.conv_p = np.array([18, 1e3, 10e3, 43e3, 88.5e3, 11e4, 15e4, 18.5e4, 22e4]) # [Pa]
        self.conv_T = np.array([40, 50, 60, 70, 80, 90, 100]) # [Cº]
        self.conv_T = self.conv_T + 273.15 # [K]

        self.intp = interpolate.interp2d(self.conv_p, self.conv_T, self.conv_h)

    
    # Plot Data
    # Reviewed: CORRECT DATA ENTRY! (Félix Martí Valverde - 16/03/2022)
    def plot_h (self):

        for i in range(self.conv_h.shape[0]):
            plt.plot(self.conv_p, self.conv_h[i, :], label = "T{} = {}ºC".format(i, self.conv_T[i]-273.15))
            plt.scatter(self.conv_p, self.conv_h[i, :])
        
        plt.legend(loc="upper left")
        plt.show()
    

    # Heat Transfer Coefficient
    # source: http://www.iaeng.org/publication/WCE2010/WCE2010_pp1444-1447.pdf

    # METHOD 1
    # Reviewed: CORRECT! (Félix Martí Valverde - 16/03/2022)
    def get_h (self, h, T):

        p = self.get_p(h)
        return self.intp(p, T)


    # METHOD 2
    # Review: ERROR in interpolation, better use scipy tools (METHOD 1)! (Félix Martí Valverde - 16/03/2022)
    def get_h_2 (self, h, T):

        index_p = -1
        index_T = -1

        # Index Temperature
        for i in range(len(self.conv_T)):
            if self.conv_T[i] > T:
                index_T = i
                break
        
        # Index Pressure
        p = self.get_p(h)
        for i in range(len(self.conv_p)):
            if self.conv_p[i] > p:
                index_p = i
                break
        
        if index_p == -1 or index_T == -1:
            print("error")
            return -1

        if index_p == len(self.conv_p)-1 or index_T == len(self.conv_T)-1:
            print("error")
            return -1

        # Convection Coefficients (T-p)
        h11 = self.conv_h[index_T, index_p]
        h12 = self.conv_h[index_T, index_p+1]
        h21 = self.conv_h[index_T+1, index_p]
        h22 = self.conv_h[index_T+1, index_p+1]

        dT = self.conv_T[index_T+1] - self.conv_T[index_T]
        dp = self.conv_p[index_p+1] - self.conv_p[index_p]

        # P const.
        dhdT_p1 = (h21 - h11) / dT
        dhdT_p2 = (h22 - h12) / dT

        # Interpolation
        h1 = h11 + dhdT_p1 * (T - self.conv_T[index_T])
        h2 = h12 + dhdT_p2 * (T - self.conv_T[index_T])

        # T const.
        dhdp = (h2 - h1) / dp

        # Interpolation
        h_ = h1 + dhdp * (p - self.conv_p[index_p])

        return h_


if __name__ == "__main__":

    atmos   = Atmosphere()
    cyl     = Cylinder()

    T_check = 0
    P_check = 0
    D_check = 0
    h_check = 1

    # NOTE: Height tested up to 80 km in steps of 100 meters
    it      = 800
    step    = 100

    Temp = 26.43 + 273.15

    """ TEMPERATURE CHECK """
    if T_check: 
        T = np.zeros(it)
        for i in range(it):
            T[i] = atmos.get_T(i*step)

        plt.plot(T-273.15, np.linspace(0, it*step, it))
        plt.show()

    """ PRESSURE CHECK """
    if P_check:
        P = np.zeros(it)
        for i in range(it):
            P[i] = atmos.get_p(i*step)

        plt.plot(P, np.linspace(0, it*step, it))
        plt.show()

    """ DENSITY CHECK """
    if D_check:
        D = np.zeros(it)
        for i in range(it):
            D[i] = atmos.get_density(i*step)

        plt.plot(D, np.linspace(0, it*step, it))
        plt.show()

    """ HEAT TRANSFER COEFFICIENT CHECK """
    if h_check:

        cyl.plot_h()

        h = np.zeros(it)
        for i in range(it):
            h[i] = cyl.get_h(i*step, Temp)

        plt.plot(h, np.linspace(0, it*step, it))
        plt.scatter(h, np.linspace(0, it*step, it))
        plt.show()