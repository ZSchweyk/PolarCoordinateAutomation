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


def convert_to_cartesian(theta, r):
    return r * cos(theta), r * sin(theta)


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

    draw_polar(
        (screen_size.width / 2 - 400, screen_size.height / 2),
        "3 * sin(4 * theta)",
        [0, 2 * pi, pi / 80],
        (-3, 3),
        (-3, 3),
        (-350, 350),
        (-350, 350)
    )


def draw_polar(origin: tuple, equation: str, np_arange_args: list, x_orig: tuple, y_orig: tuple, x_scaled: tuple,
               y_scaled: tuple):
    pyautogui.moveTo(origin[0], origin[1])
    pyautogui.leftClick()

    global is_program_running
    global continue_drawing

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

    previous_cart_1 = ()
    previous_cart_2 = ()

    for theta1 in np.arange(np_arange_args[0], (np_arange_args[1] / 2 + .01), np_arange_args[2]):
        if continue_drawing == 1:
            theta2 = theta1 + pi
            r1 = eval(equation.replace("theta", "theta1"))
            r2 = eval(equation.replace("theta", "theta2"))

            x1, y1 = convert_to_cartesian(theta1, r1)
            x2, y2 = convert_to_cartesian(theta2, r2)

            x1 = scale(x1, x_orig[0], x_orig[1], x_scaled[0], x_scaled[1])
            y1 = scale(y1, y_orig[0], y_orig[1], y_scaled[0], y_scaled[1])

            x2 = scale(x2, x_orig[0], x_orig[1], x_scaled[0], x_scaled[1])
            y2 = scale(y2, y_orig[0], y_orig[1], y_scaled[0], y_scaled[1])

            x1 += origin[0]
            y1 += origin[1]

            x2 += origin[0]
            y2 += origin[1]

            print(f"{(r1 >= 0) == (r2 >= 0)}")

            # print(f"r1: {r1 >= 0}", end=" ")
            # print(f"r2: {r2 >= 0}")
            # print(f"{r2=}")
            # print(f"theta1 = {theta1 * 180/pi}")
            # print(f"theta2 = {theta2 * 180/pi}")


            if previous_cart_1 == () and previous_cart_2 == ():
                previous_cart_1 = (x1, y1)
                previous_cart_2 = (x2, y2)

            pyautogui.moveTo(previous_cart_1[0], previous_cart_1[1])
            pyautogui.dragTo(x1, y1, duration=.025)

            pyautogui.moveTo(previous_cart_2[0], previous_cart_2[1])
            pyautogui.dragTo(x2, y2, duration=.025)

            previous_cart_1 = x1, y1
            previous_cart_2 = x2, y2

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
