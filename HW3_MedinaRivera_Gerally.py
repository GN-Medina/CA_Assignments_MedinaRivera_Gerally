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
G = 6.674e-11        # m^3 kg^-1 s^-2
M_EARTH = 5.972e24   # kg
M_MOON = 7.348e22   # kg
R = 3.844e8         # m
OMEGA = 2.662e-6    # s^-1

def f(r):
    return ((G*M_EARTH)/r**2) - ((G*M_MOON)/(R - r)**2) - OMEGA**2 * r

def f_der(r):
    return -2*((G*M_EARTH)/r**3) - 2*((G*M_MOON)/(R - r)**3) - OMEGA**2

def newtons_method(function, derivative, guess, tolerance=1e-10):
    """
    Function that uses Newton's method to find one solution of the given function

    Args:
        function (function): equation that will be solved
        derivative (function): analytical derivative of the equation that will be solved
        guess (float): initial guess of the solution
        tolerance (float): accuracy of the answer

    Returns:
        solution to the equation
    """

    err = 100

    while err > tolerance:
        temp = guess - (function(guess)/derivative(guess))
        err = np.abs(temp - guess)
        guess = temp

    return guess

def secant_method(function, guess_1, guess_2, tolerance=1e-10):
    """
    Function that uses secant method to find one solution of the given function

    Args:
        function (function): equation that will be solved
        guess_1 (float): first starting guess
        guess_2 (float): second starting guess
        tolerance (float): accuracy of the answer

    Returns:
        solution to the equation
    """

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
    parser.add_argument('method', type=str, default='Newton', help="Method used to numerically solve the equation. It can be Newton's method or secant method.")
    parser.add_argument('--plot-first', action='store_true', help='If used, it shows a plot a the function and asks the user to input their guess for the solution.')
    parser.add_argument('--r-Nguess', type=float, default=3.5e8, help="Initial distance guess for Newton's method. Default is 3.5e8 meters.")
    parser.add_argument('--r-sguess-1', type=float, default=3e8, help='First starting value for secant method. Default is 3e8 meters.')
    parser.add_argument('--r-sguess-2', type=float, default=3.5e8, help='Second starting value for secant method. Default is 3.5e8 meters.')
    parser.add_argument('--tol', type=float, default=1e-4, help='Accuracy of answer. Default is 1e-4.')

    args = parser.parse_args()

    if args.plot_first:
        x = np.arange(6.3e6, R, 0.03e8)
        y = f(x)

        plt.plot(x,y)
        plt.axhline(y=0, color='black', linestyle='--')
        plt.ylim(-0.05, 0.05)

        plt.xlabel('x [m]', fontsize=12, labelpad=8, fontstyle='italic')
        plt.ylabel('y', fontsize=12, labelpad=8, fontstyle='italic')
        plt.title(r'$f(x) = \frac{GM}{r^2} - \frac{Gm}{(R - r)^2} - \omega^2 r = 0$', fontsize=14, pad=15, weight='bold')
        plt.show()

        if args.method[0].lower() == 'n':
            user_guess = float(input('What is your guess for the distance of the L\u2081 Lagrange point? '))
            dist = newtons_method(f, f_der, user_guess, args.tol)

        elif args.method[0].lower() == 's':
            user_guess_1 = float(input('What is your first guess for the distance of the L\u2081 Lagrange point? '))
            user_guess_2 = float(input('What is your second guess for the distance of the L\u2081 Lagrange point? '))
            dist = secant_method(f, user_guess_1, user_guess_2, args.tol)

        else:
            sys.exit('The method entered is not valid. Use "-h" or "-help" to view which methods are supported.')


    else:

        if args.method[0].lower() == 'n':
            dist = newtons_method(f, f_der, args.r_Nguess, args.tol)

        elif args.method[0].lower() == 's':
            dist = secant_method(f, args.r_sguess_1, args.r_sguess_2, args.tol)

        else:
            sys.exit('The method entered is not valid. Use "-h" or "-help" to view which methods are supported.')

    print('')
    print(f'The distance from Earth to the L\u2081 Lagrange point is {dist:.3e} meters.')
    print('')

# End of Code