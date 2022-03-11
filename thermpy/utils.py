import numpy as np

'''
r: Ratio Cylinder [m]
b: Length Cylinder [m]
'''
def surface_cyl (r, b):
    return 2 * np.pi * r * b

''' [checked]
res: List of All Resistances in Parallel [/]
'''
def parallel_resistance (res):
    par = 0
    for r in res:
        par += 1 / r
    return 1 / par

# CONSTANTS
global rad_const
rad_const = 5.67e-8