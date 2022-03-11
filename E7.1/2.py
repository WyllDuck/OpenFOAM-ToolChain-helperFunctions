from math import log, sqrt

Di = 0.025
den = 1.01
Pr = 0.7179
T_0i = 310
T_m = 350

k_m = 0.0297
press_L = 300
Re = 28717

Cf = 1 / pow(1.58 * log(Re) - 3.28, 2)
print("Cf = {:.9f}".format(Cf))

f = T_m / T_0i
p_ = 0.38
G = sqrt(press_L * Di * den / (2 * Cf * pow(f, p_)))
print("G = {:.9f}".format(G))

n_ = 0.36
aux = Cf * (Re - 1000) * Pr * pow(f, n_)
Nu = aux / (2 + 17.96 * pow(Cf, 0.5) * (pow(Pr, 2/3) - 1))
print("Nu = {:.4f}".format(Nu))

h = Nu * k_m / Di
print("h = {:.4f}".format(h))

