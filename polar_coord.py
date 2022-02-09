import pyautogui
import time
from math import *
import numpy as np
from pynput import keyboard
from threading import Thread
from sympy import *

continue_drawing = 0
resume = True
is_program_running = True


def scale(value, v_min, v_max, r_min, r_max):
    percentage = (value - v_min) / (v_max - v_min)
    return round(r_min + percentage * (r_max - r_min), 2)


def on_release(key):
    draw_func = Thread(target=polar_equations)
    global is_program_running
    global continue_drawing
    global resume
    if is_program_running:
        if key == keyboard.Key.enter:
            continue_drawing = 1
            draw_func.start()
        elif key == keyboard.Key.esc:
            continue_drawing = 2
        elif key == keyboard.Key.space:
            resume = not resume
            continue_drawing = 3


def polar_equations():
    screen_size = pyautogui.size()
    print(screen_size)

    # draw_polar(
    #     (screen_size.width / 2, screen_size.height / 2),
    #     "8",
    #     [0, 2 * pi, pi / 1000],
    #     (-8, 8),
    #     (-8, 8),
    #     (-350, 350),
    #     (-350, 350)
    # )
    for a in range(-1, -16, -2):
        draw_y_equals_a((screen_size.width / 2 - 500, screen_size.height / 2 - 50), a, [-5, 5])


def draw_polar(origin: tuple, equation: str, np_arange_args: list, x_orig: tuple, y_orig: tuple,
               x_scaled: tuple, y_scaled: tuple):

    pyautogui.moveTo(origin[0], origin[1])
    pyautogui.leftClick()


    global is_program_running
    global continue_drawing
    count = 0

    builtin_restrictions = {
        "min": min,
        "max": max,
    }
    other_restrictions = {
        "sqrt": sqrt,
        "sin": sin,
        "cos": cos,
    }

    theta = 0
    other_restrictions["theta"] = theta
    try:
        eval(equation, {"__builtins__": builtin_restrictions}, other_restrictions)
    except Exception as exception:
        print("Invalid Input!")
        print(exception)
        is_program_running = False
        return

    # print(np.arange(np_arange_args[0], (np_arange_args[1] + .01), np_arange_args[2]))

    for theta in np.arange(np_arange_args[0], (np_arange_args[1] + .01), np_arange_args[2]):
        if continue_drawing == 1:
            r = eval(equation)

            x = r * cos(theta)
            y = r * sin(theta)

            x = scale(x, x_orig[0], x_orig[1], x_scaled[0], x_scaled[1])
            y = scale(y, y_orig[0], y_orig[1], y_scaled[0], y_scaled[1])

            x += origin[0]
            y += origin[1]

            print((x, y))

            if count == 0:
                pyautogui.moveTo(x, y)
            # elif count % 20 == 0:
            #     time.sleep(2)
            else:
                pyautogui.dragTo(x, y, duration=.025)
            count += 1
        elif continue_drawing == 2:
            print("Drawing was stopped.")
            is_program_running = False
            return
        elif continue_drawing == 3:
            global resume
            while not resume:
                pass
            else:
                continue_drawing = 1
    print("Completed drawing the polar equation!")
    is_program_running = False
    return


def draw_y_equals_a(origin: tuple, a: float, boundaries: list):
    x1, x2 = boundaries
    r = f"{a} / sin(theta)"
    eval_acot = lambda x, a: acot(x / a)
    theta1 = (eval_acot(x1, a) + pi) if eval_acot(x1, a) < 0 else eval_acot(x1, a)
    theta2 = (eval_acot(x2, a) + pi) if eval_acot(x2, a) < 0 else eval_acot(x2, a)

    if a >= 0:
        draw_polar(
            origin,
            r,
            [min(theta1, theta2), max(theta1, theta2), pi / 196],
            (x1, x2),
            (0, 15),
            (-200, 200),
            (0, -350)
        )
    else:
        draw_polar(
            origin,
            r,
            [min(theta1, theta2), max(theta1, theta2), pi / 196],
            (x1, x2),
            (0, -15),
            (-200, 200),
            (0, 350)
        )

def draw_x_equals_a(origin: tuple, a: float, boundaries: list):
    y1, y2 = boundaries
    r = f"{a} / cos(theta)"



# equations = [
#     "10 + 2 * sin(62 * theta)",
#     "12",
#     "8",
#     "7 + sin(50 * theta)",
#     "6",
#     "5 + .8 * sin(25 * theta)",
#     "4"
# ]
#
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()
