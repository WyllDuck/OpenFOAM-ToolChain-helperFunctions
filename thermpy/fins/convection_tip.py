import numpy as np
from . import fin

'''
m: Fin Parameter [/]
---
L: Fin Length [m]
Ac: Cross Sectional Area Fin [m^2]
P: Perimeter Cross Sectional Area [m]
'''
def efficiency (m, L, Ac, P):
    L_ = L + Ac / P
    return np.tanh(m * L_) / (m * L_)

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

    a = h / (m * k)
    num = np.sinh(m * L) + a * np.cosh(m * L)
    den = np.cosh(m * L) + a * np.sinh(m * L)

    return M * num / den

'''
m: Fin Parameter [/]
---
x: Position Temperature [m]
L: Fin Length [m]
'''
def T_distribution_unitary (m, x, L):

    a = h / (m * k)
    num = np.cosh(m * (L - x)) + a * np.sinh(m * (L - x))
    den = np.cosh(m * L) + a * np.sinh(m * L)

    return num / den