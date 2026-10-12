"""
Gerally Medina Rivera

Homework 4 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

# Imports

import argparse
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

# Functions

def dft(f, N):
    """
    Discrete Fourier transform function to calculate the Fourier coefficients.

    Args:
        f (array_like): Real-valued data expected to be sampled at evenly spaced points.
        N (int): Number of values in the given array.

    Returns:
        coef_arr (np.array): Fourier coefficients for the given function.
    """

    coef_arr = np.zeros(N // 2 + 1, complex)

    for k in range(N // 2 + 1):
        for n in range(N):
            coef_arr[k] += f[n] * np.exp(-2j * np.pi * k * n / N)

    return coef_arr

def inv_transform(c_arr, kmax, N):
    """
    Inverse Fourier transform to obtain back the values of the function.

    Args:
        c_arr (array_like): Values of the Fourier coefficients.
        kmax (int): Maximum value of the coefficients to be used for the inverse transform.
        N (int): Number of values in the given array.

    Returns:
        y_arr (np.array): Evenly spaced values of the function given the Fourier coefficients.
    """

    y_arr = np.zeros(N, complex)

    for n in range(N):
        for k in range(kmax + 1):
            if k == 0:
                weight = 1
            else:
                weight = 2     # Doubles the negative frequencies
            y_arr[n] += (weight/N) * c_arr[k] * np.exp(2j * np.pi * k * n / N)

    return y_arr

# Main Code

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--fn', type=str, default='tic0040244907.fits',
                        help="Filename of the FITS file to be used. This code assumes it is in the same directory as "
                             "the script.")
    parser.add_argument('--mask-min', type=float, default=2769,
                        help="Minimum value used to truncate the time interval. Default is the Julian Date 2769. "
                             "Other suggested values are 3310 or 3505.")
    parser.add_argument('--mask-max', type=float, default=2828,
                        help="Maximum value used to truncate the time interval. Default is the Julian Date 2828. "
                             "Other suggested values are 3370 or 3560.")
    parser.add_argument('--ps-max', type=float, default=200,
                        help="Maximum value of the k interval used for the x limit of the Power Spectrum plot. "
                             "High k values should flatten to zero, so constricting the x limits helps visualize the "
                             "spectrum better. Default is 200.")
    parser.add_argument('--k-max', type=int, default=100,
                        help="Maximum value of the k interval used to create the inverse transform. "
                             "It should be where the power spectrum flattens. Default is 100.")
    parser.add_argument('--save-plots', action='store_true',
                        help="If used, saves all the plots to the code's directory.")

    args = parser.parse_args()

    # Opening the FITS file
    filename = f'./{args.fn}'
    hdul = fits.open(filename)
    times = hdul[1].data['times']     # shape = 54646
    fluxes = hdul[1].data['fluxes']   # shape = 54646

    # Truncating the times and fluxes array to the given interval
    mask = (times >= args.mask_min) & (times <= args.mask_max)

    times_slice = times[mask]
    fluxes_slice = fluxes[mask]

    # Linear Interpolation
    dt = np.median(np.diff(times_slice))    # np.diff to not take into account big chunks of no data
    t_slice_uniform = np.arange(times_slice[0], times_slice[-1], dt)
    f_slice_uniform = np.interp(t_slice_uniform, times_slice, fluxes_slice)

    # Plotting the Light Curve
    plt.scatter(t_slice_uniform, f_slice_uniform, s=3, color='royalblue')
    plt.xlabel('Truncated Barycentric Julian Date')
    plt.ylabel('Normalized PDC flux')
    plt.title('Light Curve of TIC 0040244907')
    plt.tight_layout()
    if args.save_plots:
        plt.savefig(f'LightCurve_{args.fn}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Calculating the Fourier coefficients
    N = len(t_slice_uniform)
    c = dft(f_slice_uniform, N)

    power = np.abs(c)**2
    index = np.arange(N // 2 + 1)

    # Plotting the Power Spectrum
    plt.plot(index, power, color='royalblue')
    plt.xlim(1, args.ps_max)
    plt.ylim(0, np.max(power[1:]))
    plt.xlabel('k (cycles per time)')
    plt.ylabel('Power')
    plt.title('Power Spectrum of TIC 0040244907')
    plt.tight_layout()
    if args.save_plots:
        plt.savefig(f'PowerSpectrum_{args.fn}.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Calculating the period of the eclipse based on the harmonics
    k_peak = np.argmax(power[1:])
    fundamental = k_peak/2                          # k_peak is divided by two because it is the second harmonic
    total_time = t_slice_uniform[-1] - t_slice_uniform[0]
    period = total_time/fundamental
    print(f"According to the power spectrum, the period of this eclipsing binary is {period:.3f} days. The value in the "
          f"TESS EB catalog is 3.318 days.")

    # Calculating the inverse transform with different coefficients

    def invtrans_plot(c_arr, kmax, n, N):

        y = inv_transform(c_arr, kmax, N)

        axs[n].plot(t_slice_uniform, y.real, color='royalblue', lw=1)
        axs[n].set_title(f'inverse transform, k ≤ {kmax}')

    # Plotting the light curve with different inverse transforms

    fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(7, 8), sharex=True, sharey=True,
                        constrained_layout=True)

    axs[0].plot(t_slice_uniform, f_slice_uniform, '.', ms=2, color='black')
    axs[0].set_title('Data')

    invtrans_plot(c, int(np.ceil(fundamental)), 1, N)
    invtrans_plot(c, int(np.ceil(fundamental*2)), 2, N)
    invtrans_plot(c, int(np.ceil(fundamental*3)), 3, N)
    invtrans_plot(c, int(args.k_max), 4, N)

    axs[0].set_ylim(-0.05, 1.35)
    fig.suptitle('Light Curve of TIC 0040244907', fontsize=14)
    fig.supxlabel('Truncated Barycentric Julian Date')
    fig.supylabel('Normalized PDC flux')
    if args.save_plots:
        plt.savefig(f'LightCurve_wInverseTransform_{args.fn}.png', dpi=300, bbox_inches='tight')
    plt.show()

# End of Code