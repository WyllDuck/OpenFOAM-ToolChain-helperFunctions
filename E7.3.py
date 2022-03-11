import thermpy as th
from math import log, pi, exp

# DECLARE VALUES/PARAMETERS
# ---- START ----

a = 0.03
b = 0.02
t = 0.002
L = 0.4

P_ini = 200
T_ini = 20 + 273.15
u_ini = 12

k_p = 40

T_v = 100 + 273.15
h_v = 2550
h_lv = 2257

cp = 1004

Nf = 4

n_ = 0.47
p_ = 0.52

T_fin = 330 # SOLO PARA 1era PARTE
T_s = 340 # SOLO PARA 1era PARTE

def den_d (T, P): return 3.484 * P / T
def k_d (T): return (3.807 + 0.074 * T) * 1e-3
def mu (T, P): return (2.469 + 0.0536 * T + P / 8280) * 1e-6 

# ---- END ----

# DECLARE EQUATIONS 
def main():
# ---- START ----

    Lf = (b - 3 * t) * 0.5
    print("Lf = {:.4f}".format(Lf))

    P_h = (4 * Lf) * 4
    print("P_h = {:.4f}".format(P_h))

    S_h = pow(Lf, 2) * 4 
    print("S_h = {:.7f}".format(S_h))

    D_h = 4 * S_h / P_h
    print("1) D_h = {:.5f}".format(D_h))
    print()

    T_m = 0.5 * (T_fin + T_ini)
    print("T_m = {:.4f}".format(T_m))

    # Calculo de h_out
    G = u_ini * den_d(T_ini, P_ini)
    print("G = {:.8f}".format(G))

    Re = G * D_h / mu(T_m, P_ini)
    print("2) Re = {:.4f}".format(Re))
    print()

    Pr = cp * mu(T_m, P_ini) / k_d(T_m)
    print("Pr = {:.8f}".format(Pr))

    Cf = 1 / pow(1.58 * log(Re) - 3.28, 2)
    print("Cf = {:.4f}".format(Cf))
    
    f = T_m / T_s
    aux = Cf * (Re - 1000) * Pr * (1 + pow(D_h / L, 2/3)) * pow(f, n_)
    Nu = aux / (2 + 17.96 * pow(Cf, 0.5) * (pow(Pr, 2/3) - 1))
    print("Nu = {:.4f}".format(Nu))

    h_out = Nu * k_d(T_m) / D_h
    # P_t == P_h |Como son iguales no necesitamos aplicar ningun factor corrector
    print("3) h_out = {:.4f}".format(h_out))
    print()

    # FIN
    m = th.fins.fin.parameter(h_out, k_p, 2 * L, t * L)
    ef = th.fins.adiabatic_tip.efficiency(m, Lf)
    print("ef = {:.4f}".format(ef))

    # RESISTENCIAS
    Am = (b - t) * 4 * L
    r_tot = th.res.wall(t, Am, k_p) + th.res.convection(h_v, b * L * 4)
    
    A_pri = (2 * Lf * L) * Nf
    A_sec = (2 * Lf * L)
    
    r_fin = th.res.thermal_resistance_with_efficiency(ef, A_sec, Nf, h_out)
    r_n_fin = th.res.convection(h_out, A_pri)
    r_eq = th.parallel_resistance([r_fin, r_n_fin])
    
    r_tot += r_eq
    print("r_tot = {:.4f}".format(r_tot))

    U0 = 1 / ((b * L * 4)* r_tot )
    print("4) U0 = {:.4f}".format(U0))
    print()

    m_dot = u_ini * S_h * den_d(T_ini, P_ini)
    q_total = m_dot * cp * (T_fin - T_ini)
    print("5) q_total = {:.4f}".format(q_total))
    print()

    delta_pres = 2 * Cf * pow(f, p_) * L / D_h * pow(G, 2) / den_d(T_ini, P_ini)
    print("delta_pres = {:.5f}".format(delta_pres))
    
    P_aire = u_ini * S_h * delta_pres
    print("6) P_aire = {:.4f}".format(P_aire))
    print()



# FASE 2: Iterativa
def iter (T_s, T_fin):

    # REPETIR CALCULOS PRIMERA PARTE
    Lf = (b - 3 * t) * 0.5
    print("Lf = {:.4f}".format(Lf))

    P_h = (4 * Lf) * 4
    print("P_h = {:.4f}".format(P_h))

    S_h = pow(Lf, 2) * 4 
    print("S_h = {:.7f}".format(S_h))

    D_h = 4 * S_h / P_h
    print("D_h = {:.5f}".format(D_h))
    print()

    T_m = 0.5 * (T_fin + T_ini)
    print("T_m = {:.4f}".format(T_m))

    # Calculo de h_out
    G = u_ini * den_d(T_ini, P_ini)
    print("G = {:.8f}".format(G))

    Re = G * D_h / mu(T_m, P_ini)
    print("Re = {:.4f}".format(Re))

    Pr = cp * mu(T_m, P_ini) / k_d(T_m)
    print("Pr = {:.8f}".format(Pr))

    Cf = 1 / pow(1.58 * log(Re) - 3.28, 2)
    print("Cf = {:.4f}".format(Cf))
    
    f = T_m / T_s
    aux = Cf * (Re - 1000) * Pr * (1 + pow(D_h / L, 2/3)) * pow(f, n_)
    Nu = aux / (2 + 17.96 * pow(Cf, 0.5) * (pow(Pr, 2/3) - 1))
    print("Nu = {:.4f}".format(Nu))

    h_out = Nu * k_d(T_m) / D_h
    # P_t == P_h |Como son iguales no necesitamos aplicar ningun factor corrector
    print("h_out = {:.4f}".format(h_out))
    print()

    # FIN
    m = th.fins.fin.parameter(h_out, k_p, 2 * L, t * L)
    ef = th.fins.adiabatic_tip.efficiency(m, Lf)
    print("ef = {:.4f}".format(ef))

    # RESISTENCIAS
    Am = (b - t) * 4 * L
    r_tot = th.res.wall(t, Am, k_p) + th.res.convection(h_v, b * L * 4)
    
    A_pri = (2 * Lf * L) * Nf
    A_sec = (2 * Lf * L)
    
    r_fin = th.res.thermal_resistance_with_efficiency(ef, A_sec, Nf, h_out)
    r_n_fin = th.res.convection(h_out, A_pri)
    r_eq = th.parallel_resistance([r_fin, r_n_fin])
    
    r_tot += r_eq
    print("r_tot = {:.4f}".format(r_tot))

    U0 = 1 / ((b * L * 4)* r_tot )
    print("U0 = {:.4f}".format(U0))
    print()

    m_dot = u_ini * S_h * den_d(T_ini, P_ini)

    ####################
    # CALCULOS 2nd PARTE
    ####################
    
    T_fin_new = T_v + (T_ini - T_v) * exp(-U0 * (b * L * 4) / (m_dot * cp))
    print("7) T_fin_new = {:.4f}".format(T_fin_new))
    print()

    delta_T = ((T_v - T_ini) - (T_v - T_fin_new)) / log((T_v - T_ini) / (T_v - T_fin_new))
    q = U0 * (b * 4 * L) * delta_T
    print("q = {:.4f}".format(q))

    T_s_new = - q * (r_tot - r_eq) + T_v
    print("8) T_s_new = {:.4f}".format(T_s_new))
    print()

    q_total_new = m_dot * cp * (T_fin_new - T_ini)
    print("9) q_total_new = {:.4f}".format(q_total_new))
    print()

    delta_pres_new = 2 * Cf * pow(f, p_) * L / D_h * pow(G, 2) / den_d(T_ini, P_ini)
    print("delta_pres_new = {:.5f}".format(delta_pres_new))
    
    P_aire_new = u_ini * S_h * delta_pres_new * den_d(T_ini, P_ini) / den_d(T_fin_new, P_ini)
    print("10) P_aire_new = {:.4f}".format(P_aire_new))
    print()

    m_cond = q / h_lv * 3600
    print("11) m_cond = {:.4f}".format(m_cond))
    print()

    return T_s_new, T_fin_new


# ---- END ----

if __name__ == "__main__":

    main()

    """
    print("################################################")
    print("################################################")
    print()
    print("                  ITERATION PROCESS")
    print()
    print("################################################")
    print("################################################")

    i = 0 # iteration
    print("iteration: {}\n".format(i))

    # Initial Guest

    T_s_old = T_s
    T_fin_old = T_fin

    T_s_new, T_fin_new = iter(T_s_old, T_fin_old)

    while abs(T_s_old - T_s_new) > 0.1 or abs(T_fin_old - T_fin_new) > 0.1:

        i += 1
        print("\n ======================================= \n")
        print("iteration: {}\n".format(i))
        
        T_s_old = T_s_new
        T_fin_old = T_fin_new

        T_s_new, T_fin_new = iter(T_s_old, T_fin_old)


"""