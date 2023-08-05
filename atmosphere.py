import numpy as np
import matplotlib.pyplot as plt
from math import exp


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

        self.h_interpolate      = np.array([-1000, 0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000, 70000, 80000])  # [m]
        self.T_interpolate      = np.array([21.5, 15, 8.5, 2, -4.49, -10.98, -17.47, -23.96, -30.45, -36.94, -43.42, -49.9, -56.5, -56.5, -51.6, -46.64, -22.8, -2.5, -26.13, -53.57, -74.51]) + 273.15 # [K]
        self.P_interpolate      = np.array([11.39, 10.13, 8.988, 7.95, 7.012, 6.166, 5.405, 4.722, 4.111, 3.565, 3.08, 2.65, 1.211, 0.5529, 0.2549, 0.1197, 0.0287, 0.007978, 0.002196, 0.00052, 0.00011]) * 1e4 # [Pa]
        self.rho_interpolate    = np.array([1.347, 1.225, 1.112, 1.007, 0.9093, 0.8194, 0.7364, 0.6601, 0.59, 0.5258, 0.4671, 0.4135, 0.1948, 0.08891, 0.04008, 0.01841, 0.003996, 0.001027, 0.0003097, 0.00008283, 0.00001846]) # [kg/m3]
        self.mu_interpolate     = np.array([1.821, 1.789, 1.758, 1.726, 1.694, 1.661, 1.628, 1.595, 1.561, 1.527, 1.493, 1.458, 1.422, 1.422, 1.448, 1.475, 1.601, 1.704, 1.584, 1.438, 1.321]) * 1e-5 # [Ns/m2] 
    
    
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
    

    # Interpolated Functions
    def get_T_interpolate (self, h):
        return np.interp(h, self.h_interpolate, self.T_interpolate)

    def get_P_interpolate (self, h):
        return np.interp(h, self.h_interpolate, self.P_interpolate)

    def get_density_interpolate (self, h):    
        return np.interp(h, self.h_interpolate, self.rho_interpolate)

    def get_mu_interpolate (self, h):
        return np.interp(h, self.h_interpolate, self.mu_interpolate)


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


if __name__ == "__main__":

    atmos   = Atmosphere()

    T_check     = 1
    P_check     = 1
    D_check     = 1
    mu_check    = 1

    # NOTE: Height tested up to 80 km in steps of 100 meters
    it      = 800
    step    = 100

    """ TEMPERATURE CHECK """
    if T_check: 
        T = np.zeros(it)
        T_interpolate = np.zeros(it)
        for i in range(it):
            T[i] = atmos.get_T(i*step)
            T_interpolate[i] = atmos.get_T_interpolate(i*step)

        plt.plot(T-273.15, np.linspace(0, it*step, it), label="T")
        plt.plot(T_interpolate-273.15, np.linspace(0, it*step, it), label="T_interpolate")
        
        plt.title("Temperature")
        plt.xlabel("Temperature [K]")
        plt.ylabel("Height [m]")
        plt.legend()
        plt.grid()
        plt.show()

    """ PRESSURE CHECK """
    if P_check:
        P = np.zeros(it)
        P_interpolate = np.zeros(it)
        for i in range(it):
            P[i] = atmos.get_p(i*step)
            P_interpolate[i] = atmos.get_P_interpolate(i*step)

        plt.plot(P, np.linspace(0, it*step, it), label="P")
        plt.plot(P_interpolate, np.linspace(0, it*step, it), label="P_interpolate")
        
        plt.title("Pressure")
        plt.xlabel("Pressure [Pa]")
        plt.ylabel("Height [m]")
        plt.legend()
        plt.grid()
        plt.show()

    """ DENSITY CHECK """
    if D_check:
        D = np.zeros(it)
        D_interpolate = np.zeros(it)
        for i in range(it):
            D[i] = atmos.get_density(i*step)
            D_interpolate[i] = atmos.get_density_interpolate(i*step)

        plt.plot(D, np.linspace(0, it*step, it), label="D")
        plt.plot(D_interpolate, np.linspace(0, it*step, it), label="D_interpolate")
        
        plt.title("Density")
        plt.xlabel("Density [kg/m^3]")
        plt.ylabel("Height [m]")
        plt.legend()
        plt.grid()
        
        plt.show()

    """ VISCOSITY CHECK """
    if mu_check:
        mu_interpolate = np.zeros(it)
        for i in range(it):
            mu_interpolate[i] = atmos.get_mu_interpolate(i*step)

        plt.plot(mu_interpolate, np.linspace(0, it*step, it), label="mu_interpolate")
        
        plt.title("Viscosity")
        plt.xlabel("Viscosity [Pa*s]")
        plt.ylabel("Height [m]")
        plt.legend()
        plt.grid()
        
        plt.show()