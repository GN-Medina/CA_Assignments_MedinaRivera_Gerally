"""
Gerally Medina Rivera

Homework 2 for Computational Astrophysics
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
    parser.add_argument('--save-plot', action='store_true', help='If used, saves plot to folder.')

    args = parser.parse_args()

    x = np.arange(args.x_llimit, args.x_ulimit+args.x_step, args.x_step)
    y = E(x, args.slices)

    # Plot
    plt.plot(x, y, color='orangered', linewidth=1.3)

    plt.xlim(args.x_llimit, args.x_ulimit)
    plt.ylim(bottom=0,top=None)

    plt.xlabel('x', fontsize=12, labelpad=8, fontstyle='italic')
    plt.ylabel('y', fontsize=12, labelpad=8,fontstyle='italic')
    plt.title(r'$E(x) = \int_{0}^{x} e^{t^{2}} dt$', fontsize=14, pad=15, weight='bold')

    plt.grid(linestyle=':', alpha=0.7)

    if args.save_plot == True:
        plt.savefig('function_plot.png', dpi=300, bbox_inches='tight')

    plt.show()

# End of Code