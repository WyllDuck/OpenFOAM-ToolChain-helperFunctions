import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


# Rocket
class Rocket (object):

    def __init__ (self):

        self.t      = [0, 10, 50, 80, 105, 120, 180, 200, 300, 400, 500, 600, 700, 800, 1000]
        self.alt    = [0, 10e3, 35e3, 45e3, 47e3, 43e3, 30e3, 27e3, 17.5e3, 13e3, 8e3, 5.5e3, 3e3, 1.3e3, 0]

        self.intp   = interpolate.interp1d(self.t, self.alt) 


    # Get Current Altitude
    # input: time [sec.] | output: height [m]
    def get_altitude (self, t):
        return self.intp(t)


    def plot (self):

        plt.plot(self.t, self.alt)
        plt.show()


if __name__ == "__main__":
    
    rocket = Rocket()
    rocket.plot()

    # Test Altitude Function
    alt = np.zeros(1000)

    for t in range(1000):
        alt[t] = rocket.get_altitude(t)

    plt.plot(alt)
    plt.show()
