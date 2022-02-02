import pyautogui
import time
import math
import numpy as np

time.sleep(3)


def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)


def draw(origin: tuple, equation: str, num_rot: float, increment: float, x_orig: tuple, y_orig: tuple,
         x_scaled: tuple, y_scaled: tuple):
    pyautogui.moveTo(origin[0], origin[1])

    count = 0
    for theta in np.arange(0, (num_rot * 2 + .01) * math.pi, increment):
        r = eval(equation)
        x = r * math.cos(theta)
        y = r * math.sin(theta)

        x = scale(x, x_orig[0], x_orig[1], x_scaled[0], x_scaled[1])
        y = scale(y, y_orig[0], y_orig[1], y_scaled[0], y_scaled[1])

        x += origin[0]
        y += origin[1]

        # print((x, y))

        if count == 0:
            pyautogui.moveTo(x, y)
        else:
            pyautogui.dragTo(x, y, duration=.025)
        count += 1


screen_size = pyautogui.size()

print(screen_size)

draw((screen_size.width / 2 - 200, screen_size.height / 2), "theta * math.cos(theta)", 6, math.pi / 192, (0, 37.7), (-18.46, 17.6735),
     (-350, 350), (-350, 350))
