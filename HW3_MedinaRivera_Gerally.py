"""
Gerally Medina Rivera

Homework 3 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

# Imports

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt

# Functions
G = 6.67e-11        # m^3 kg^-1 s^-2
M_EARTH = 5.97e24   # kg
M_MOON = 7.348e22   # kg
R = 3.844e8         # m
OMEGA = 2.662e-6    # s^-1

def f(r):
    return ((G*M_EARTH)/r**2) - ((G*M_MOON)/(R - r)**2) - OMEGA**2 * r

def f_der(r):
    return -2*((G*M_EARTH)/r**3) - 2*((G*M_MOON)/(R - r)**3) - OMEGA**2

def newtons_method(function, derivative, guess, tolerance=1e-10):
    err = 100

    while err > tolerance:
        temp = guess - (function(guess)/derivative(guess))
        err = np.abs(temp - guess)
        guess = temp

    return guess

def secant_method(function, guess_1, guess_2, tolerance=1e-10):
    err = 100

    while err > tolerance:
        temp = guess_2 - function(guess_2)*((guess_2 - guess_1)/(function(guess_2)-function(guess_1)))

        err = np.abs(temp - guess_2)
        guess_1 = guess_2
        guess_2 = temp

    return guess_2

# Main Code

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('method', type=str, default='Newton', help="Method used to numerically solve the equation. It can be Newton's or secant method.")
    parser.add_argument('--r-Nguess', type=float, default=3.5e8, help="Initial distance guess for Newton's method. Default is 3.5e8 meters.")
    parser.add_argument('--r-sguess-1', type=float, default=3e8, help='First starting value for secant method. Default is 3e8 meters.')
    parser.add_argument('--r-sguess-2', type=float, default=3.5e8, help='Second starting value for secant method. Default is 3.5e8 meters.')
    parser.add_argument('--tol', type=float, default=1e-4, help='Accuracy of answer. Default is 1e-4.')

    args = parser.parse_args()

    if args.method[0].lower() == 'n':
        dist = newtons_method(f, f_der, args.r_Nguess, args.tol)

    elif args.method[0].lower() == 's':
        dist = secant_method(f, args.r_sguess_1, args.r_sguess_2, args.tol)

    else:
        sys.exit('The method entered is not valid. Use "-h" or "-help" to view which methods are supported.')

    print(f'The distance from Earth to the L\u2081 Lagrange point is {dist:.4e} meters.')
# End of Code