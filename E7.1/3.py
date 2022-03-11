from math import pi

Nt = 3
De = 60/1000
D0 = 24/1000
Di = 22/1000
Nu = 60
km = 0.0271
cp = 1004
mu = 1.94e-5

S_h = pi / 4 * pow(De, 2) - 3 * pi / 4 * pow(D0, 2)
print("S_h = {:.9f}".format(S_h))

P_h = pi * De + 3 * pi * D0
print("P_h = {:.9f}".format(P_h))

P_t = 3 * pi * D0
print("P_t = {:.9f}".format(P_t))

D_h = 4 * S_h / P_h
print("D_h = {:.9f}".format(D_h))

Pr = mu * cp / km
print("Pr = {:.9f}".format(Pr))

h = Nu * km / D_h
h = h * (1 - 0.75 / (1 + Pr) * (1 - P_t / P_h))
print("h = {:.9f}".format(h))
