import thermpy as th
import numpy as np
import matplotlib.pyplot as plt


"""
AUXILIARY FUNCTIONS
"""

# Find Current Stage
def find_index (time, t_stages):
    sum_ = 0
    for i in range(len(t_stages)):
        sum_ += t_stages[i]
        if sum_ > time:
            return i
    return len(t_stages) - 1


"""
DATA
"""

# Configuration Battery
s = 7 # series
p = 2 # parallel

# Cell Parameters
cap_cell    = 650e-3            # Capacity Cell [Ah]
R_int       = 80e-3             # Internal Resistance Cell [ohms]
V_cell      = (4.2 + 2.75) / 2  # Voltage Cell [V]

# Mission Stages
t_stages    = [0, 88, 26.5, 7, 23.5, 3, 767, 3, 72]     # duration of each stage [sec.]
t_total     = sum(t_stages)                             # total duration of mission [sec.]

w_stages    = [120, 48, 96, 48, 0, 20, 0, 20, 48]       # consumption in each stage [W]
w_static    = 27.21                                     # Static Power Consumption [W]


"""
MAIN
"""
def main ():

    # Saved Values
    Q_data = []
    W_data = []
    t_data = []

    time    = 0
    dt      = 0.01 # step

    while time < t_total:

        i = find_index(time, t_stages)

        W = w_stages[i] + w_static  # power demand of the system
        I = W / (V_cell * s)        # intensity demand based on battery voltage

        # Heat Dissipated [W]
        Q_cell = pow((I / p), 2) * R_int
        Q_bat = s * p * Q_cell

        # Save Data
        Q_data.append(Q_bat)
        W_data.append(W)
        t_data.append(time)

        time += dt # next step

    plot(Q_data, t_data)
    plot(W_data, t_data)


"""
PLOT
"""
def plot (Q_data, t_data):
    plt.plot(t_data, Q_data)
    plt.show()


if __name__ == "__main__":
    main()