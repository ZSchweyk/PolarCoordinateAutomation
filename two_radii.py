from math import *
import numpy as np


def convert_to_cartesian(theta, r):
    return r * cos(theta), r * sin(theta)


equation = "sin(4 * theta)"

for theta1 in np.arange(0, pi, pi / 192):
    theta2 = theta1 + pi

    r1 = eval(equation.replace("theta", "theta1"))
    r2 = eval(equation.replace("theta", "theta2"))

    print("r1:", r1)
    print("r2:", r2)

print("Done drawing", equation)
