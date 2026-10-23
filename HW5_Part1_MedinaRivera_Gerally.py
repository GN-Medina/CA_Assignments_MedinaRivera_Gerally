"""
Gerally Medina Rivera

Homework 5 - Part 1 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

# Imports

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Functions

def step(l, r):
    return -l * np.log(1 - r)

def photon_path(initial_theta=1, rng=np.random.default_rng()):
    """
    define

    Args:
        initial_theta (float):
        rng (Generator):

    Returns:
        z_arr (list):
        theta_arr (list):
    """
    z = step(l, rng.random()) * initial_theta    # initial step inside the slab

    z_arr = [0,z]
    theta_arr = [initial_theta]

    while 0 < z < 1000:
        theta = 2*rng.random() - 1        # cosine
        new_z = z + step(l, rng.random()) * theta

        z_arr.append(new_z)
        theta_arr.append(theta)

        z = new_z

    return z_arr, theta_arr

# Main Code

if __name__ == '__main__':
    n_e = 1e20                 # cm^-3
    sigma_T = 6.652e-25        # cm^2
    l = (1/(n_e*sigma_T))/100  # m

    z_arr, theta_arr = photon_path()

    # Plot

    if z_arr[-1] < 0:
        z_arr[-1] = 0
    elif z_arr[-1] > 1000:
        z_arr[-1] = 1000

    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(xlim=(-50,1050),ylim=(0,len(z_arr)))

    ax.invert_yaxis()
    ax.axvline(0)
    ax.axvline(1000)
    ax.axvspan(0, 1000, alpha=0.2, color='gray')

    ax.set_ylabel('Scattering Number')
    ax.set_xlabel('Depth z [m]')

    line, = ax.plot([],[])
    steps = range(len(z_arr))

    def animate(i):
        line.set_data(z_arr[:i+1], steps[:i+1])

    anim = animation.FuncAnimation(fig, animate, frames=len(z_arr), interval=200)

    writergif = animation.PillowWriter(fps=5)
    anim.save('filename.gif', writer=writergif)

    plt.show()

# End of Code