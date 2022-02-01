import pyautogui
import time
import math
import numpy as np


def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)


time.sleep(15)

origin = (1000, 950)

pyautogui.moveTo(origin[0], origin[1])

count = 0
for theta in np.arange(0, 10.01 * math.pi, math.pi / 96):
    r = 7 + math.cos(10.2 * theta)
    x = r * math.cos(theta)
    y = r * math.sin(theta)

    x = scale(x, -8, 8, -300, 300)
    y = scale(y, -8, 8, -300, 300)

    x += origin[0]
    y += origin[1]

    print((x, y))

    if count == 0:
        pyautogui.moveTo(x, y)
    else:
        pyautogui.dragTo(x, y, duration=.1)
    count += 1
