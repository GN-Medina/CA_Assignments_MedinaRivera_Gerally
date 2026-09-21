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

def f(t):
    return np.e**(-t**2)

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

def E(x,N):
    return simps_rule(f,0,x,N)

# Main Code

if __name__ == '__main__':
    x = np.arange(0,3.1,0.1)
    y = E(x, 10)

# End of Code