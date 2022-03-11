import numpy as np
from . import fin

'''
h: Heat Transfer Coefficient [W/m^2·K]
k: Thermal Conductivity [W/m·K]
---
Ac: Cross Sectional Area Fin [m^2]
P: Perimeter Cross Sectional Area [m]
---
T0: Temperature Base [K or ºC]
Tinf: Temperature Fluid [K or ºC]
'''
def q(h, k, Ac, P, T0, Tinf):
    return (T0 - Tinf) * np.sqrt(P * Ac * k * h)

'''
m: Fin Parameter [/]
---
x: Position Temperature [m]
'''
def T_distribution_unitary (m, x):
    return np.exp(- m * x)