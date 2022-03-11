import thermpy as th
from scipy.optimize import fsolve
import numpy as np

N = 64

tf = 1e-3

Lf = 4e-3
Ld = 1e-3
Lc = 1e-3
Lb = 0.5e-3

g = 1.2e7 # dif

kd = 380
kc = 20
kb = 0.24

r_tc = 0.02

Tinf_i = 35
Tinf_s = 30

hi = 12
hs = 120

def calculate():

    print()
    print("PART A")

    biot = (hs * tf/4) / kd
    print("1) biot = {:.8f}".format(biot))

    m = np.sqrt((hs * 4) / (kd * tf))
    print("2) m = {:.2f}".format(m))

    lc2 = tf / 4 * 2
    rend = np.tanh(m * lc2) / (m * lc2)
    print("3) rend = {:.10f}".format(rend))

    G = g * (16 * tf) * (16 * tf) * Lc
    print("4) G = {:.2f}".format(G))

    ########
    print()

    r_pi = Lb / (kb * (16 * tf) * (16 * tf))
    r_hi = 1 / ((16 * tf) * (16 * tf) * hi)

    r_eq_i = r_pi + r_hi + r_tc / (16e-3 * 16e-3)
    print("5) r_eq_i = {:.2f}".format(r_eq_i))

    Af = 4 * tf * Lf + tf * tf
    r_f = 1 / (N * Af * rend * hs)
    
    Anf = (16 * tf) * (16 * tf) - tf * tf * N
    r_nf = 1 / (Anf * hs)

    r_ps = Ld / (kd * (16 * tf) * (16 * tf))

    r_eq_s = (r_nf * r_f) / (r_nf + r_f) + r_ps
    print("6) r_eq_s = {:.2f}".format(r_eq_s))

    ###################
    print()
    print("PART B")






if __name__ == "__main__":

    calculate()
    