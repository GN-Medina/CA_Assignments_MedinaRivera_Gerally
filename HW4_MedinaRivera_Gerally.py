"""
Gerally Medina Rivera

Homework 4 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

# Imports

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

# Functions

# Main Code

if __name__ == '__main__':

    filename = './tic0040244907.fits'
    hdul = fits.open(filename)
    times = hdul[1].data['times']     # 54646
    fluxes = hdul[1].data['fluxes']   # 54646
    ferrs = hdul[1].data['ferrs']     # 54646

    mask = (times >= 2769) & (times <= 2828)

    times_slice = times[mask]
    fluxes_slice = fluxes[mask]
    ferrs_slice = ferrs[mask]

    N = len(times_slice)
    c = np.zeros(N // 2 + 1, complex)

    for k in range(N // 2 + 1):
        for n in range(N):
            c[k] += fluxes_slice[n] * np.exp(-2j * np.pi * k * n / N)

    index = np.arange(N // 2 + 1)

    plt.plot(index, np.abs(c)**2)
    plt.xlim(1)
    plt.ylim(0, 1e5)
    plt.show()

    y = np.zeros(N, complex)

    for n in range(N):
        for k in range(N // 2 + 1):
            y[n] += (1/N) * c[k] * np.exp(2j * np.pi * k * n / N)

    plt.plot(times_slice, y.real)
    plt.show()

'''
    plt.scatter(times_slice, fluxes_slice)
    
    1660, 1745
    2417.5, 2447.5
    2768, 2828
    3310, 3370
    3505, 3560
    
    plt.show()
'''

'''
See how few coefficients you can use to capture the behavior...?
Linear interpolation?
 
'''

# End of Code