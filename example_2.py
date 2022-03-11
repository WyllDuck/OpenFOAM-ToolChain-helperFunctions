import thermpy as th
from scipy.optimize import fsolve
import numpy as np

# DECLARE VALUES/PARAMETERS
# ---- START ----
Tinf = 20
T1 = 60

h = 50

N = 12
t = 2e-3
b = 0.6
r_tc = 1e-3

ka = 0.5
kf = 15
kb = 1.5

r1 = 10e-3
r2 = 12e-3
r3 = 17e-3
r4 = 40e-3
# ---- END ----

# DECLARE EQUATIONS 
def func(x):
# ---- START ----
    
    # UNKNOWS
    T3 = x[0]

    # EQUATIONS
    r_tot = th.res.cyl(r2, r3, b, kf) + th.res.cyl(r1, r2, b, ka) + r_tc / th.utils.surface_cyl(r1, b)
    L = r4 - r3

    P = 2 * b
    Ac = b * t
    m = th.fins.fin.parameter(h, kf, P, Ac)
    
    q_f = N * th.fins.fixed_tip_temperature.q(m, h, kf, Ac, P, L, Tinf, T3, Tinf)
    q_nf = h * (T3 - Tinf) * (th.utils.surface_cyl(17e-3, 0.6) - (N * t * b))

    return [(T1 - T3) / r_tot - q_f - q_nf]

# ---- END ----

if __name__ == "__main__":
    root = fsolve(func, [0])
    print(root)
    