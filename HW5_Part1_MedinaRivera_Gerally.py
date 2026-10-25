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
    """
    Transformed probability equation that calculates the length of step a photon takes in a medium with a mean free path
    of l.

    Args:
        l (float): Mean free path value of the area the photon is traversing.
        r (float): Random number from [0,1) to be transformed inta a step length the same units as the mean free path.

    Returns:
        Length of step the photon takes in the same units as the mean free path.
    """

    return -l * np.log(1 - r)

def photon_path(l, width_slab, initial_theta=0, rng=np.random.default_rng()):
    """
    Function that calculates the path of a photon through a slab of given thickness and a constant electron density.

    Args:
        l (float): Mean free path value of the area the photon is traversing.
        width_slab (float): Thickness of the slab.
        initial_theta (float): The angle in radians the photon enters the slab with, the default is 0 rad.
        rng (Generator): Random number generator used to sample step length and scattering direction.

    Returns:
        z_list (list): Values of the depth of the photon.
        cos_theta_list (list): Values of cos(theta) the photon used in its path.
    """

    z = step(l, rng.random()) * np.cos(initial_theta)    # initial step inside the slab

    z_list = [0,z]
    cos_theta_list = [np.cos(initial_theta)]

    while 0 < z < width_slab:
        cos_theta = 2*rng.random() - 1        # cosine
        new_z = z + step(l, rng.random()) * cos_theta

        z_list.append(new_z)
        cos_theta_list.append(cos_theta)

        z = new_z

    return z_list, cos_theta_list

# Main Code

if __name__ == '__main__':
    n_e = 1e20                 # cm^-3
    sigma_T = 6.652e-25        # cm^2
    l = (1/(n_e*sigma_T))/100  # ~ 150 m

    z_list, cos_theta_list = photon_path(l, 1000)

    # Plot

    # Clip the end of the photon's path so it stops cleanly as 0 or 1000
    if z_list[-1] < 0:
        z_list[-1] = 0
    elif z_list[-1] > 1000:
        z_list[-1] = 1000

    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(ylim=(-50,1050),xlim=(0,len(z_list)))

    ax.axhline(0, color='black', linewidth=2)
    ax.axhline(1000, color='black', linewidth=2)
    ax.axhspan(0, 1000, alpha=0.2, color='gray')

    ax.set_xlabel('Scattering Number')
    ax.set_ylabel('Depth z [m]')

    line, = ax.plot([],[], color='goldenrod')
    dot, = ax.plot([], [], 'o', color='darkgoldenrod')
    steps = range(len(z_list))

    def animate(i):
        line.set_data(steps[:i+1], z_list[:i+1])
        dot.set_data([steps[i]], [z_list[i]])

    anim = animation.FuncAnimation(fig, animate, frames=len(z_list), interval=200)

    writergif = animation.PillowWriter(fps=5)
    #anim.save('filename.gif', writer=writergif)

    plt.show()

# End of Code