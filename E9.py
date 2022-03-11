from math import *
import numpy as np

D1 = 0.2
W = 1.0
H = 1.75

A1 = pi * D1
A2 = pi * W / 2
A3 = W
A4 = 2 * H

F11 = 0  # CORRECTO
F12 = 0.5  # CORRECTO
F13 = (2 * atan((0.5 * W) / H)) / (2 * pi) # CORRECTO
F14 = (2 * atan(H / (0.5 * W))) / (2 * pi) # CORRECTO

F41 = F14 * A1 / A4 # CORRECTO
F31 = F13 * A1 / A3 # CORRECTO
F21 = F12 * A1 / A2 # CORRECTO

X = W / H
F34 = 1 - (pow(1 + pow(X, 2), 0.5) - 1) / X # CORRECTO
F43 = F34 * A3 / A4 # CORRECTO

F33 = 0 # CORRECTO
F32 = 1 - F31 - F33 - F34 # CORRECTO
F23 = F32 * A3 / A2 # CORRECTO

Aaux = 2 * sqrt(pow(D1/2, 2) + pow(W/2, 2))
F22 = 1 - Aaux / A2
F24 = 1 - F21 - F22 - F23

F42 = F24 * A2 / A4
F44 = 1 - F41 - F42 - F43

res = np.array([[F11, F12, F13, F14], [F21, F22, F23, F24], [F31, F32, F33, F34], [F41, F42, F43, F44]])
print(res.round(3))

# Verificacion
print(np.sum(res[0, :]))
print(np.sum(res[1, :]))
print(np.sum(res[2, :]))
print(np.sum(res[3, :]))