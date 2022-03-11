"""
Aquí tiene el problema completamente solucionado con un programa de Python.
No tengo tiempo de pasarlo ha escrito, lo siento mucho. He intentado ser lo 
más claro posible en la redacción, dado que no hay una opción escrita a mano.

Si instala SciPy (o ya lo tiene instalado junto con Python) este programa 
debería funcionar sin problemas.

He verificado todos los resultados que obtengo con el programa dan igual que 
en la solución después de 6 iteraciones, lo cual es mucha precisión.

Espero que con este problema resuelto ayude.

=====================================================

AQUI TIENE EL "OUTPUT" DEL PROGRAMA EN MI ORDENADOR

 =======================================

iteration: 0
Tm = 318.15
Pm = 100825.00

-- den = 1.10411535
k = 0.02735010
mu = 0.00001953
cp = 1004.00000000

-- phi = 0.85
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 29459.61786648
-- Cf = 0.00593593
-- G = 22.65608954

-- m_dot = 0.1722
-- u = 20.5197
Pr = 0.71707793

Nu = 67.09
-- h = 72.24

r_tot = 0.00231310
5) U0 = 72.24

-- q_total = 13831.12
Tf_new = 365.35635


 =======================================

iteration: 1
Tm = 321.75
Pm = 100825.00

-- den = 1.09175084
k = 0.02761674
mu = 0.00001973
cp = 1004.00000000

-- phi = 0.86
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 28848.83356924
-- Cf = 0.00596633
-- G = 22.40571604

-- m_dot = 0.1703
-- u = 20.5227
Pr = 0.71717586

Nu = 66.37
-- h = 72.16

r_tot = 0.00231566
5) U0 = 72.16

-- q_total = 14910.40
Tf_new = 365.54988


 =======================================

iteration: 2
Tm = 321.85
Pm = 100825.00

-- den = 1.09142260
k = 0.02762390
mu = 0.00001973
cp = 1004.00000000

-- phi = 0.86
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 28832.69102762
-- Cf = 0.00596714
-- G = 22.39906620

-- m_dot = 0.1702
-- u = 20.5228
Pr = 0.71717847

Nu = 66.35
-- h = 72.16

r_tot = 0.00231573
5) U0 = 72.16

-- q_total = 14939.05
Tf_new = 365.55501


 =======================================

iteration: 3
Tm = 321.85
Pm = 100825.00

-- den = 1.09141391
k = 0.02762409
mu = 0.00001973
cp = 1004.00000000

-- phi = 0.86
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 28832.26345158
-- Cf = 0.00596716
-- G = 22.39889004

-- m_dot = 0.1702
-- u = 20.5228
Pr = 0.71717854

Nu = 66.35
-- h = 72.16

r_tot = 0.00231573
5) U0 = 72.16

-- q_total = 14939.81
Tf_new = 365.55514


 =======================================

iteration: 4
Tm = 321.85
Pm = 100825.00

-- den = 1.09141368
k = 0.02762409
mu = 0.00001973
cp = 1004.00000000

-- phi = 0.86
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 28832.25212550
-- Cf = 0.00596717
-- G = 22.39888537

-- m_dot = 0.1702
-- u = 20.5228
Pr = 0.71717854

Nu = 66.35
-- h = 72.16

r_tot = 0.00231573
5) U0 = 72.16

-- q_total = 14939.83
Tf_new = 365.55515


 =======================================

iteration: 5
Tm = 321.85
Pm = 100825.00

-- den = 1.09141367
k = 0.02762409
mu = 0.00001973
cp = 1004.00000000

-- phi = 0.86
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 28832.25182548
-- Cf = 0.00596717
-- G = 22.39888525

-- m_dot = 0.1702
-- u = 20.5228
Pr = 0.71717854

Nu = 66.35
-- h = 72.16

r_tot = 0.00231573
5) U0 = 72.16

-- q_total = 14939.83
Tf_new = 365.55515


 =======================================

iteration: 6
Tm = 321.85
Pm = 100825.00

-- den = 1.09141367
k = 0.02762409
mu = 0.00001973
cp = 1004.00000000

-- phi = 0.86
P_h = 1.20
-- P_t = 1.20
S_h = 0.00760061
-- D_h = 0.02540

SOLVE
-- Re = 28832.25181753
-- Cf = 0.00596717
-- G = 22.39888524

-- m_dot = 0.1702
-- u = 20.5228
Pr = 0.71717854

Nu = 66.35
-- h = 72.16

r_tot = 0.00231573
5) U0 = 72.16

-- q_total = 14939.83
Tf_new = 365.55515

-- caudal_f = 0.1780
-- caudal_m = 0.1560
-- P_util = 156
-- P_req = 195
"""


from math import log, pi, exp
from scipy.optimize import fsolve

# DECLARE VALUES/PARAMETERS
# ---- START ----

# Geometria
Ds  = 127e-3
D   = 25.4e-3
N = 10
L = 5

# Entrada Aire
Ti = 5 + 273.15
Pi = 1 * 101325
delta_P = 1000 # caida de presion

# Vapor Saturado a 1atm
Tv = 100 + 273.15
Pv = 1 * 101325

# Propiedades Vapor (T: Kelvin / P: Pa)
def f_den (T, P): return 3.484 * P / T * 1e-3
def f_k (T): return (3.807 + 0.074 * T) * 1e-3
def f_mu (T, P): return (2.469 + 0.0536 * T + P * 1e-3 / 8280) * 1e-6 
def f_cp (): return 1004

# ---- END ----

# AUXILIARY FUNCTIONS
# ---- START ----

def func(x):
    
    # UNKNOWS
    Re = x[0]
    Cf = x[1]
    G = x[2]

    f0 = (G * D_h / mu) - Re
    f1 = (1 / pow((1.58 * log(Re) - 3.28), 2)) - Cf
    f2 = (2 * Cf * pow(letra_rara, p) * L * pow(G, 2) / (D_h * den)) - delta_P

    return [f0, f1, f2]

# ---- END ----

# DECLARE EQUATIONS 
def find(Tf):
# ---- START ----

    global D_h, mu, letra_rara, p, den, m_dot, Tm, Pm

    # Propiedades del Aire
    Tm = (Ti + Tf) / 2
    Pm = Pi - 0.5 * delta_P

    print("Tm = {:.2f}".format(Tm))
    print("Pm = {:.2f}".format(Pm))

    print()

    den =   f_den(Tm, Pm)
    k =     f_k(Tm)
    mu =    f_mu(Tm, Pm)
    cp =    f_cp()

    print("-- den = {:.8f}".format(den))
    print("k = {:.8f}".format(k))
    print("mu = {:.8f}".format(mu))
    print("cp = {:.8f}".format(cp))

    print()

    # Tablas - aire que se calienta
    letra_rara = Tm / Tv
    p = 0.52
    n = 0.47

    print("-- phi = {:.2f}".format(letra_rara))

    # Geometria
    P_h = pi * (Ds + N * D)
    print("P_h = {:.2f}".format(P_h))

    P_t = pi * (Ds + N * D)
    print("-- P_t = {:.2f}".format(P_t))

    S_h = pi / 4 * (pow(Ds, 2) - N * pow(D, 2))
    print("S_h = {:.8f}".format(S_h))

    D_h = 4 * S_h / P_h
    print("-- D_h = {:.5f}".format(D_h))
    print()

    # Flujo
    root = fsolve(func, [10000, 10e-3, 10])
    Re, Cf, G = root

    print("SOLVE")
    print("-- Re = {:.8f}".format(Re))
    print("-- Cf = {:.8f}".format(Cf))
    print("-- G = {:.8f}".format(G))

    print()

    m_dot = G * S_h
    print("-- m_dot = {:.4f}".format(m_dot))

    u = m_dot / (den * S_h)
    print("-- u = {:.4f}".format(u))

    Pr = cp * mu / k
    print("Pr = {:.8f}".format(Pr))

    print()

    aux = Cf * (Re - 1000) * Pr * (1 + pow(D_h / L, 2/3)) * pow(letra_rara, n)
    Nu = aux / (2 + 17.96 * pow(Cf, 0.5) * (pow(Pr, 2/3) - 1))
    print("Nu = {:.2f}".format(Nu))

    h = Nu * k / D_h
    # h = h * (1 - 0.75 / (1 + Pr) * (1 - P_t / P_h)) # Apply corrector factor P_h != P_t
    print("-- h = {:.2f}".format(h))
    print()

    # Calor de Convection
    r_tot = 1 / (h * P_h * L)
    print("r_tot = {:.8f}".format(r_tot))

    U0 = 1 / ((P_h * L) * r_tot )
    print("5) U0 = {:.2f}".format(U0))
    print()

    q_total = m_dot * cp * (Tf - Ti)
    print("-- q_total = {:.2f}".format(q_total))

    Tf_new = Tv + (Ti - Tv) * exp(- (U0 * P_h * L) / (m_dot * cp)) 
    print("Tf_new = {:.5f}".format(Tf_new))
    print()

    return Tf_new

# ---- END ----

if __name__ == "__main__":

    i = 0 # iteration
    print("\n ======================================= \n")
    print("iteration: {}".format(i))

    # Initial Guest
    Tf_old = Ti + 80

    Tf_new = find(Tf_old)

    while abs(Tf_old - Tf_new) > 1e-8:

        i += 1
        print("\n ======================================= \n")
        print("iteration: {}".format(i))
        
        Tf_old = Tf_new

        Tf_new = find(Tf_old)

    # DESPUES DE ITERAR - OTRAS PREGUNTAS
    den_f = f_den(Tf_new, Pi - delta_P)

    caudal_f = m_dot / den_f
    print("-- caudal_f = {:.4f}".format(caudal_f))

    den_m = f_den(Tm, Pm)

    caudal_m = m_dot / den_m
    print("-- caudal_m = {:.4f}".format(caudal_m))

    P_util = (caudal_m) * delta_P
    print("-- P_util = {:.0f}".format(P_util))

    P_req = P_util / 0.8
    print("-- P_req = {:.0f}".format(P_req))

    


