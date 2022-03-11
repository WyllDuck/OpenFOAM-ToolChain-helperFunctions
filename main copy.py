import thermpy as th
from scipy.optimize import fsolve
import numpy as np

# DECLARE VALUES/PARAMETERS
# ---- START ----
# ---- END ----

# DECLARE EQUATIONS 
def func(x):
# ---- START ----
    
    # UNKNOWS
    T0 = x[0]
    e = x[1]*2 + 0.022

    # EQUATIONS
    r_tot = th.res.cyl(0.02, 0.022, 1, 80) + th.res.cyl(0.022, e, 1, 0.04) + th.res.convection(15e3, np.pi * 0.020)
    
    q_rad = 5.67e-8 * 0.6 * (pow(273.15 + T0, 4) - pow(273.15 + 10, 4))
    q_conv = (T0 - 25) * (1.31 * pow((T0 - 25) / e, 0.25))
    
    f1 = (110 - T0) / r_tot
    f2 = (q_rad + q_conv) * (np.pi * e)

    return [f1 - 20, f2 - 20]

# ---- END ----

if __name__ == "__main__":
    root = fsolve(func, [100, 0.1e-3])
    print(root)
    