# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt, pow

# Others
from atmosphere import Atmosphere 


""" MAIN """
def main ():

    Uatm = 20
    Iatm = 0.008
    eddy_viscosity_ratio = 0.7 # 0.2 - 1.3 for external flows

    # Simulation Objects
    atmos = Atmosphere()

    # NOTE: Height tested up to 80 km in steps of 100 meters
    it      = 20000
    step    = 1

    rho = np.zeros(it)
    mu  = np.zeros(it)
    c   = np.zeros(it)

    gamma  = 1.4
    
    R       = 8.31446261815324 # [J/(mol*K)]
    M_air   = 0.0289644 # [kg/mol]
    Rs      = R/M_air

    # fixed values
    Re  = 9.84e6
    D   = 1 # Measurements per meter!

    for i in range(it):
        rho[i] = atmos.get_density_interpolate(i*step)
        mu[i]  = atmos.get_mu_interpolate(i*step)
        c[i]   = np.sqrt(gamma*Rs*atmos.get_T_interpolate(i*step))

    # Reynolds Number (Re = rho*U*D/mu)
    # Re - Reynolds Number
    # rho - Density
    # U - Velocity
    # D - Characteristic Length
    # mu - Dynamic Viscosity

    U = Re/(rho*D/mu)
    Ma = U/c

    # PLOT
    plt.plot(U, np.linspace(0, it*step, it), label="U")
    plt.plot(c, np.linspace(0, it*step, it), label="c")
    
    plt.xlabel("Velocity [m/s]")
    plt.ylabel("Height [m]")
    plt.legend()
    plt.show()

    plt.plot(Ma, np.linspace(0, it*step, it), label="Ma")

    plt.xlabel("Mach Number")
    plt.ylabel("Height [m]")

    # RASAERO values proposed
    h_RASAERO   = np.array([1, 25000, 30500, 33000, 37000, 44000, 59000, 63000]) * 0.3048 # Height [m]
    Ma_RASAERO  = np.array([0.42, 0.9, 1.05, 1.2, 1.5, 2.0, 4.0, 5.0]) # Mach Number

    plt.scatter(Ma_RASAERO, h_RASAERO, label="RASAERO Study Points")

    plt.legend()
    plt.grid()
    plt.show()


    # Calculate Boundary Conditions for Project Mach Numbers
    Ma_PROJECT = [0.6, 0.8, 0.9, 0.95, 1.0, 1.2, 1.5, 1.8, 2.3, 2.96, 3.96, 4.63]

    data = np.zeros((len(Ma_PROJECT), 10))

    for i in range(len(Ma_PROJECT)):

        index = np.absolute(Ma - Ma_PROJECT[i]).argmin()

        h = index*step
        T = atmos.get_T_interpolate(h)
        p = atmos.get_P_interpolate(h)
        u = Ma_PROJECT[i] * np.sqrt(gamma*Rs*T)
        r = atmos.get_density_interpolate(h)
        mu = atmos.get_mu_interpolate(h)

        # Turbulent Kinetic Energy
        # Variables: Turbulent Intersity Atmosphere (Iatm), Speed Atmosphere (Uatm)
        k = sqrt(3/2) * (Uatm * Iatm) ** 2

        # Turbulent Dissipation Rate
        w = (r * k / mu) * pow(eddy_viscosity_ratio, -1)

        data[i, 0] = h
        data[i, 1] = T
        data[i, 2] = p
        data[i, 3] = u
        data[i, 4] = Ma_PROJECT[i]
        data[i, 5] = r
        data[i, 6] = 0 # Knudsen Number
        data[i, 7] = mu
        data[i, 8] = k
        data[i, 9] = w

    print(data)

    plt.plot(Ma, np.linspace(0, it*step, it), label="Ma")
    plt.scatter(Ma_PROJECT, data[:, 0], label="PROJETC Study Points")

    plt.xlabel("Mach Number")
    plt.ylabel("Height [m]")

    plt.legend()
    plt.grid()
    plt.show()

    Kn = np.array(Ma_PROJECT)/Re * np.sqrt(gamma * np.pi / 2)
    data[:, 6] = Kn

    # Save Data
    df = pd.DataFrame(data, columns=["Height [m]", "Temperature [K]", "Pressure [Pa]", "Velocity [m/s]", "Mach Number [-]", "Density [kg/m^3]", "Knudsen Number [-]", "Dynamic Viscosity [Pa*s]", "Turbulent Kinetic Energy [m^2/s^2]", "Turbulent Dissipation Rate [1/s]"])
    df.to_csv("boundary_conditions.csv", index=False)


if __name__ == "__main__":
    main()