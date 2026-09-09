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
    parser.add_argument('-height', type=float, help='Height of ball above ground.')
    parser.add_argument('-u', type=str, default='m', help='Units of the height. Default is meters ("m"), '
                                                                        'but can be kilometers ("km"), feet ("ft"), or '
                                                                        'inches ("in").')
    parser.add_argument('-gravity', type=float, default=9.8, help='Value of gravity the ball is subjected '
                                                                                'to in meters per seconds squared. '
                                                                                'Default is Earths gravity (9.8).')
    args = parser.parse_args()

    # in case no height is given
    if args.height == None:
        sys.exit('No value for height entered. Use "-h" or "-help" to view how to provide a value.')

    # converting any value to meters
    if args.u == 'm':
        user_height_meters = args.height
        units = 'meters'

    elif args.u == 'km':
        user_height_meters = args.height*1000
        units = 'kilometers'

    elif args.u == 'ft':
        user_height_meters = args.height/3.28
        units = 'feet'

    elif args.u == 'in':
        user_height_meters = args.height/39.37
        units = 'inches'

    else:    # in case invalid units were given
        sys.exit('The units entered are invalid. Use "-h" or "-help" to view which units can be used.')

    result = time_drop(user_height_meters, args.gravity)

    print(f'The time it takes a ball dropped from {args.height} {units} to reach the ground is {result:.2f} seconds.')

# End of Code