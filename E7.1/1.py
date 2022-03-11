T_s = 250
T_inf = 15
u_inf = 0.09

alpha = 3.872e-5
kf = 0.03383

q_A = u_inf / alpha * kf * (T_inf - T_s) 
print("q_A = {:.2f}".format(q_A))

h = q_A / (T_s - T_inf)
print("h = {:.2f}".format(h))
