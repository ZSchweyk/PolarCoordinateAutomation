import pyautogui
import time
import math
import numpy as np

time.sleep(10)

def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)

def draw(origin: tuple, coefficients: tuple, num_rot: float, increment: float, x_orig: tuple, y_orig: tuple, x_scaled: tuple, y_scaled: tuple):

    pyautogui.moveTo(origin[0], origin[1])

    count = 0
    for theta in np.arange(0, (num_rot * 2 + .01) * math.pi, increment):
        # r = coefficients[0] + coefficients[1] * math.cos(coefficients[2] * theta)
        r = theta
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        x = scale(x, x_orig[0], x_orig[1], x_scaled[0], x_scaled[1])
        y = scale(y, y_orig[0], y_orig[1], y_scaled[0], y_scaled[1])

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

draw((screen_size.width / 2 + 100, screen_size.height / 2 + 75), (7, 0, 0), 6, math.pi / 192, (-35, 37.7), (-36.15, 33), (-300, 300), (-300, 300))

