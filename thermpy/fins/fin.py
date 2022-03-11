import numpy as np

'''
k: Thermal Conductivity [W/m·K]
h: Heat Transfer Coefficient [W/m^2·K]
---
P: Heat Transfer Perimeter Fin [m]
Ac: Cross Section Area Fin [m^2]
'''
def parameter (h, k, P, Ac):
    return np.sqrt((h * P) / (k * Ac))

'''
qf: Heat Transfer Fin [W]
---
h: Heat Transfer Coefficient [W/m^2·K]
---
Acb: Cross Section Area Base [m^2]
---
Tinf: Temperature Fuild [K or ºC]
T0: Temperature Base [K or ºC]
'''
def performance (qf, h, Acb, Tinf, T0):
    return qf / (h * Acb * (T0 - Tinf))

'''
qf: Heat Transfer Fin [W]
---
h: Heat Transfer Coefficient [W/m^2·K]
---
Af: Fin Heat Transfer Area [m^2]
---
delta_T = T0 - Tinf [/]    
    · Tinf: Temperature Fuild [K or ºC]
    · T0: Temperature Base [K or ºC]
'''
def efficiency (qf, h, Af, delta_T = 1):
    return qf / (h * Acb * delta_T)