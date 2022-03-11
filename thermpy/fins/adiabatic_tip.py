import numpy as np
from . import fin

'''
m: Fin Parameter [/]
---
L: Fin Length [m]
'''
def efficiency (m, L):
    return np.tanh(m * L) / (m * L)

'''
m: Fin Parameter [/]
---
h: Heat Transfer Coefficient [W/m^2·K]
k: Thermal Conductivity [W/m·K]
---
Ac: Cross Sectional Area Fin [m^2]
P: Perimeter Cross Sectional Area [m]
L: Fin Length [m]
---
T0: Temperature Base [K or ºC]
Tinf: Temperature Fluid [K or ºC]
'''
def q(m, h, k, Ac, P, L, T0, Tinf):

    M = (T0 - Tinf) * np.sqrt(P * Ac * k * h)

    return M * np.tanh(m * L)

'''
m: Fin Parameter [/]
---
x: Position Temperature [m]
L: Fin Length [m]
'''
def T_distribution_unitary (m, x, L):
    return np.cosh(m * (L - x)) / np.cosh(m * L)