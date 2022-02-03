import pyautogui
import time
from math import *
import numpy as np
from pynput import keyboard
from threading import Thread


continue_drawing = 0
resume = True

def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)

def on_release(key):
    draw_func = Thread(target=lambda:
        draw(
            (screen_size.width / 2, screen_size.height / 2),
            "11 + 4 * cos(8.05 * theta)",
            6,
            pi / 2000,
            (-15, 15),
            (-15, 15),
            (-350, 350),
            (-350, 350)
        )
    )


    global continue_drawing
    global resume
    if key == keyboard.Key.enter:
        continue_drawing = 1
        draw_func.start()
    elif key == keyboard.Key.esc:
        continue_drawing = 2
    elif key == keyboard.Key.space:
        resume = not resume
        continue_drawing = 3


def draw(origin: tuple, equation: str, num_rot: float, increment: float, x_orig: tuple, y_orig: tuple,
         x_scaled: tuple, y_scaled: tuple):
    pyautogui.moveTo(origin[0], origin[1])

    count = 0
    global continue_drawing
    for theta in np.arange(0, (num_rot * 2 + .01) * pi, increment):
        if continue_drawing == 1:
            r = eval(equation)

            x = -r * cos(theta)
            y = r * sin(theta)

            x = scale(x, x_orig[0], x_orig[1], x_scaled[0], x_scaled[1])
            y = scale(y, y_orig[0], y_orig[1], y_scaled[0], y_scaled[1])

            x += origin[0]
            y += origin[1]

            # print((x, y))

            if count == 0:
                pyautogui.moveTo(x, y)
            # elif count % 20 == 0:
            #     time.sleep(2)
            else:
                pyautogui.dragTo(x, y, duration=.025)
            count += 1
        elif continue_drawing == 2:
            return
        elif continue_drawing == 3:
            global resume
            while not resume:
                pass
            else:
                continue_drawing = 1
    print("Completed drawing the polar equation!")
    return




screen_size = pyautogui.size()

print(screen_size)

# equations = [
#     "10 + 2 * sin(62 * theta)",
#     "12",
#     "8",l
#     "7 + sin(50 * theta)",
#     "6",
#     "5 + .8 * sin(25 * theta)",
#     "4"
# ]
#
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()


