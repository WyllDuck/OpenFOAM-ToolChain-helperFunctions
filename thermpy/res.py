import numpy as np

'''
r1: Inner Ratio Cylinder [m]
r2: Outer Ratio Cylinder [m]
k: Thermal Conductivity [W/m·K]
b: Length Cylinder [m]
'''
def cyl (r1, r2, k, b):
    return np.log(r2/r1) / (2 * np.pi * b *k)

'''
r1: Inner Ratio Cylinder [m]
r2: Outer Ratio Cylinder [m]
k: Thermal Conductivity [W/m·K]
'''
def sphere (r1, r2, k):
    return ((1 / r1) - (1 / r2)) / (4 * np.pi * k)

'''
t: Wall Thickness [m]
k: Thermal Conductivity [W/m·K]
A: Wall Area [m^2]
'''
def wall (t, A, k):
    return t / (k * A)

'''
A: Heat Transfer Surface [m^2]
h: Heat Transfer Coefficient [W/m^2·K]
'''
def convection (h, A):
    return 1 / (h * A)

'''
ef: Fin Efficiency [%] (from 0 to 1)
Af: Fin Heat Transfer Area [m^2]
N: Number of Fins
h: Heat Transfer Coefficient [W/m^2·K]
'''
def thermal_resistance_with_efficiency (ef, Af, N, h):
    return 1 / (ef * Af * N * h)