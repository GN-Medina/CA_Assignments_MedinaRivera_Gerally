"""
Gerally Medina Rivera

Homework 1 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""
# Imports

import sys
import argparse

# Functions

def time_drop(height:float, gravity:float):
    """
    Function used to calculate the time it takes an object to reach the ground from a certain height when subjected to a
    certain gravity

    Args:
        height (float): height from which the object falls
        gravity (float): gravity to which the object is subjected

    Returns:
        time (float): time it takes for the ball to reach the ground
    """

    time = ((2*height)/gravity)**(0.5)

    return time

# Main Code

if __name__ == '__main__':

    # argparse to enter values from terminal
    parser = argparse.ArgumentParser()
    parser.add_argument('height', type=float, help='Height of ball above ground.')
    parser.add_argument('-u', type=str, default='m', help='Units of the height. Default is meters, '
                                                                        'but can be kilometers, miles, feet, or '
                                                                        'inches.')
    parser.add_argument('-gravity', type=float, default=9.81, help="Value of gravity the ball is subjected "
                                                                                "to in meters per seconds squared. "
                                                                                "Default is Earth's gravity (9.81 m/s²).")
    args = parser.parse_args()

    # converting any value to meters
    if args.u[0].lower() == 'm':
        if len(args.u) == 1 or args.u[1] == 'e':
            user_height_meters = args.height
            units = 'meters'

        elif args.u[1].lower() == 'i':
            user_height_meters = args.height*1609.34
            units = 'miles'

        else:  # in case invalid units were given
            sys.exit('The units entered are invalid. Use "-h" or "-help" to view which units are supported.')

    elif args.u[0].lower() == 'k':
        user_height_meters = args.height*1000
        units = 'kilometers'

    elif args.u[0].lower() == 'f':
        user_height_meters = args.height/3.28
        units = 'feet'

    elif args.u[0].lower() == 'i':
        user_height_meters = args.height/39.37
        units = 'inches'

    else:    # in case invalid units were given
        sys.exit('The units entered are invalid. Use "-h" or "-help" to view which units are supported.')

    result = time_drop(user_height_meters, args.gravity)

    print(f'The time it takes a ball dropped from {args.height:.2f} {units} to reach the ground is {result:.2f} seconds.')

# End of Code