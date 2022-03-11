import numpy as np
from . import fin

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
TL: Temperature Tip [K or ºC]
T0: Temperature Base [K or ºC]
Tinf: Temperature Fluid [K or ºC]
'''
def q(m, h, k, Ac, P, L, TL, T0, Tinf):

    M = (T0 - Tinf) * np.sqrt(P * Ac * k * h)
    num = np.cosh(m * L) - (TL - Tinf) / (T0 - Tinf)
    den = np.sinh(m * L)

    return M * num / den

'''
m: Fin Parameter [/]
---
x: Position Temperature [m]
L: Fin Length [m]
---
TL: Temperature Tip [K or ºC]
T0: Temperature Base [K or ºC]
Tinf: Temperature Fluid [K or ºC]
'''
def T_distribution_unitary (m, x, L, TL, T0, Tinf):

    num = (TL - Tinf) / (T0 - Tinf) * np.sinh(m * x) + np.sinh(m * (L - x))
    den = np.sinh(m * L)
    return num / den