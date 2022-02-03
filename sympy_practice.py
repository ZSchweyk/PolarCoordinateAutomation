from sympy import *
# from math import *

x, r, theta = symbols("x r theta")

expr = 5*x

expr = expr.subs(x, r * cos(theta))

print(expr)

