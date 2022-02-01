import pyautogui
import time
import math
import numpy as np

time.sleep(10)

def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)

def draw(origin: tuple, coefficients: tuple, num_rot: float, increment: float, scale_vals: tuple):

    pyautogui.moveTo(origin[0], origin[1])

    count = 0
    for theta in np.arange(0, (num_rot * 2 + .01) * math.pi, increment):
        r = coefficients[0] + coefficients[1] * math.cos(coefficients[2] * theta)
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        x = scale(x, -8, 8, scale_vals[0], scale_vals[1])
        y = scale(y, -8, 8, scale_vals[0], scale_vals[1])

        x += origin[0]
        y += origin[1]

        print((x, y))

        if count == 0:
            pyautogui.moveTo(x, y)
        else:
            pyautogui.dragTo(x, y, duration=.025)
        count += 1

screen_size = pyautogui.size()

print(screen_size)

draw((screen_size.width / 2, screen_size.height / 2 - 50), (7, 7, 10), 1, math.pi / 192, (-200, 200))
