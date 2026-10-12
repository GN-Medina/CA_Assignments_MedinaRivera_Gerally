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

    plt.scatter(times_slice, fluxes_slice, s=3, color='royalblue')
    plt.xlabel('Truncated Barycentric Julian Date')
    plt.ylabel('Normalized PDC flux')
    plt.title('Light Curve of TIC 0040244907')
    plt.tight_layout()
    plt.show()

    N = len(times_slice)
    c = np.zeros(N // 2 + 1, complex)

    for k in range(N // 2 + 1):
        for n in range(N):
            c[k] += fluxes_slice[n] * np.exp(-2j * np.pi * k * n / N)

    power = np.abs(c)**2
    index = np.arange(N // 2 + 1)

    plt.plot(index, power, color='royalblue')
    plt.xlim(1, 300)                  # Higher k values are a very small and thus ignored
    plt.ylim(0, np.max(power[1:]))
    plt.xlabel('k (cycles per time)')
    plt.ylabel('Power')
    plt.title('Power Spectrum of TIC 0040244907')
    plt.tight_layout()
    plt.show()

    kmax = 200                 # Depends on where the power spectrum flattens to zero
    y = np.zeros(N, complex)

    for n in range(N):
        for k in range(kmax + 1):
            if k == 0:
                weight = 1
            else:
                weight = 2
            y[n] += (weight/N) * c[k] * np.exp(2j * np.pi * k * n / N)

    plt.scatter(times_slice, fluxes_slice, s=2, alpha=0.3, color='black', label='data')
    plt.plot(times_slice, y.real, color='royalblue', lw=1, label=f'inverse transform, k ≤ {kmax}')
    plt.xlabel('Truncated Barycentric Julian Date')
    plt.ylabel('Normalized PDC flux')
    plt.title('Light Curve of TIC 0040244907')
    plt.legend()
    plt.tight_layout()
    plt.show()

'''    
    #1660, 1745
    #2417.5, 2447.5
    #2768, 2828
    #3310, 3370
    #3505, 3560
    
Linear interpolation?
 
'''

# End of Code