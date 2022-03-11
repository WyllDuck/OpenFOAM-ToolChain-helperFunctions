import thermpy as th
from scipy.optimize import fsolve
import numpy as np

# DECLARE VALUES/PARAMETERS
# ---- START ----
Pterm = 25e3
Pmec = 15e3
Ac = 2
h1 = 10

W = 0.7
t = 0.05
kb = 0.5
Tb = 40

Lf = 0.2
Df = 0.05
kf = 380
TL = 60
h2 = 150

Tinf = 23
# ---- END ----

# DECLARE EQUATIONS 
def func(x):
# ---- START ----
    
    # UNKNOWS
    Tc = x[4]

    T0 = x[0]
    qc = x[1]
    qb = x[2]
    qe = x[3]

    # EQUATIONS
    # 1
    r_cv = th.res.convection(h1, Ac)
    f1 = (Tc - Tinf) / r_cv - qc

    # 2
    P2 = np.pi * Df
    Ac2 = np.pi / 4 * pow(Df, 2)

    m2 = th.fins.fin.parameter(h2, kf, P2, Ac2)
    f2 = th.fins.fixed_tip_temperature.q(m2, h2, kf, Ac2, P2, Lf, TL, T0, Tinf) - qe

    print(th.fins.fixed_tip_temperature.q(m2, h2, kf, Ac2, P2, Lf, TL, 376.2, Tinf))

    # 3
    r_b = th.res.wall(t, W * W, kb)
    f3 = (Tc - Tb) / r_b - qb
    
    # 4
    f4 = (Pterm - Pmec) - (qc + qe + qb)

    # 5
    r_tc = 1e-5 / Ac2
    f5 = (Tc - T0) / r_tc - qe

    return [f1, f2, f3, f4, f5]

# ---- END ----

if __name__ == "__main__":
    root = fsolve(func, [10, 10, 10, 100, 0])
    print(root)
    