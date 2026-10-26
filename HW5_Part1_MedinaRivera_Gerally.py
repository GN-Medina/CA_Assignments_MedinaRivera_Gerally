"""
Gerally Medina Rivera

Homework 5 - Part 1 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

# Imports

import argparse
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
        r (float): Random number from [0,1) to be transformed into a step length the same units as the mean free path.

    Returns:
        Length of step the photon takes in the same units as the mean free path.
    """

    return -l * np.log(1 - r)

def photon_path(l, width_slab, initial_theta=0, rng=np.random.default_rng()):
    """
    Function that calculates the path of a photon through a slab of given thickness and a constant electron density.

    Args:
        l (float): Mean free path value of the area the photon is traversing.
        width_slab (float): Thickness of the slab in, should be in the same units as the mean free path.
        initial_theta (float): The angle in radians the photon enters the slab with, the default is 0 rad.
        rng (Generator): Random number generator used to sample step length and scattering direction.

    Returns:
        z_list (list): Values of the depth of the photon. First entry is the entrance point 0, and the units are the same
                       as the mean free path.
        cos_theta_list (list): Values of cos(theta) the photon used in its path.
        outcome (str): If the photon was reflected or transmitted.
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

    if z_list[-1] <= 0:
        outcome = 'Reflected'

    elif z_list[-1] >= width_slab:
        outcome = 'Transmitted'

    return z_list, cos_theta_list, outcome

# Main Code

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--number-density', type=float, default=1e20,
                        help="Constant number density of electrons in the slab, in cm⁻³. Default is 10²⁰ cm⁻³.")
    parser.add_argument('--thickness', type=float, default=1000,
                        help="Width of the slab the photon is traversing, in meters. Default is 1000 m.")
    parser.add_argument('--min-scattering-number', type=int, default=20,
                        help="Minimum number of scatterings the photon goes through, does not count entrance and exit "
                             "points. Default is 20.")
    parser.add_argument('--outcome', choices=['transmitted', 'reflected'], default=None,
                        help="Outcome of the exit of the photon. Choices are 'transmitted' or 'reflected'.")
    parser.add_argument('--save-gif', nargs='?', const='photon_path', default=None,
                        help="If used, a gif of the photon's path will be saved to the directory the code is in. "
                             "Default filename is 'photon_path', but can be changed if a filename is given with the"
                             " argument.")

    args = parser.parse_args()

    SIGMA_T = 6.652e-25        # Thomson cross-section, cm^2
    l = (1/(args.number_density*SIGMA_T))/100  # ~ 150 m

    while True:
        z_list, cos_theta_list, p_exit = photon_path(l, args.thickness)

        n_depth = len(z_list)
        long_enough = (args.min_scattering_number <= n_depth-2)   # checks scattering number against given minimum

        wanted = (args.outcome == p_exit.lower()) or (args.outcome is None)   # checks the outcome is desired

        if long_enough and wanted:
            break

    # Plot

    # Clips end of path so the animation looks cleaner
    if p_exit == 'Reflected':
        z_list[-1] = 0

    elif p_exit == 'Transmitted':
        z_list[-1] = args.thickness

    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(ylim=(-50, args.thickness+50), xlim=(0, n_depth-1))

    ax.axhline(0, color='black', linewidth=2)
    ax.axhline(args.thickness, color='black', linewidth=2)
    ax.axhspan(0, args.thickness, alpha=0.2, color='gray')

    ax.set_xlabel('Scattering Number')
    ax.set_ylabel('Depth z [m]')
    ax.set_title(f'Path of a {p_exit} Photon')

    line, = ax.plot([],[], color='goldenrod')
    dot, = ax.plot([], [], 'o', color='darkgoldenrod')
    steps = range(n_depth)

    def animate(i):
        line.set_data(steps[:i+1], z_list[:i+1])
        dot.set_data([steps[i]], [z_list[i]])

    anim = animation.FuncAnimation(fig, animate, frames=n_depth, interval=200)

    plt.tight_layout()

    writergif = animation.PillowWriter(fps=5)
    if args.save_gif:
        anim.save(args.save_gif + '.gif', writer=writergif)

    plt.show()

# End of Code