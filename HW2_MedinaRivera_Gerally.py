"""
Gerally Medina Rivera

Homework 1 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

# Imports

import argparse
import numpy as np
import matplotlib.pyplot as plt

# Functions

def simps_rule(f, a, b, slices):
    """
    Function that uses Simpson's rule to integrate a given function

    Args:
        f (function): function that will be integrated
        a (float): lower limit of integration
        b (float): upper limit of integration
        slices (int): number of evenly spaced slices used for integration

    Returns:
        result (float): final result of the integral
    """

    h = (b-a)/(slices)
    s = f(a) + f(b)

    for k in range(1,slices):
        if k % 2 == 1:
            s += 4*f(a + k*h)
        else:
            s += 2*f(a + k*h)

    result = (h/3)*s

    return result

def f(t):
    return np.e**(-t**2)

def E(x,N):
    return simps_rule(f,0,x,N)

# Main Code

if __name__ == '__main__':

    # argparse to enter values from terminal
    parser = argparse.ArgumentParser()
    parser.add_argument('--x-llimit', type=float, default=0, help='Lower limit of the x interval.')
    parser.add_argument('--x-ulimit', type=float, default=3, help='Upper limit of the x interval.')
    parser.add_argument('--x-step', type=float, default=0.1, help='Step between x values.')
    parser.add_argument('--slices', type=float, default=10, help='Number of slices used for the integration')

    args = parser.parse_args()

    x = np.arange(args.x_llimit, args.x_ulimit+args.x_step, args.x_step)
    y = E(x, args.slices)

    # Plot
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(r'$E(x) = \int_{0}^{x} e^{t^{2}} dt$')
    plt.show()

# End of Code