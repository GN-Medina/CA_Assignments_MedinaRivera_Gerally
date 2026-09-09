"""
Gerally Medina Rivera

Homework 1 for Computational Astrophysics
ASTR 178100
Prof. A. Maller
"""

def time_drop(height:float, gravity:float =9.8):
    """
    Function used to calculate the time it takes an object to reach the ground from a certain height when subjected to a
    certain gravity

    Args:
        height (float): height, in meters, from which the object falls
        gravity (float): gravity, in meters per seconds squared, to which the object is subjected

    Returns:
        time (float): time, in seconds, it takes for the ball to reach the ground
    """

    time = ((2*height)/gravity)**(0.5)

    return time

if __name__ == '__main__':
    print('What units is your height in?')
    print('[0] meters')
    print('[1] kilometers')
    print('[2] feet')
    print('[3] inches')
    user_height_meters = None

    while not user_height_meters:
        user_units_opt = input('Enter the number of your choice: ')
        user_height = float(input('From what height does the ball drop? '))

        if user_units_opt == '0':
            user_height_meters = user_height
            units = 'meters'

        elif user_units_opt == '1':
            user_height_meters = user_height*1000
            units = 'kilometers'

        elif user_units_opt == '2':
            user_height_meters = user_height/3.28
            units = 'feet'

        elif user_units_opt == '3':
            user_height_meters = user_height/39.37
            units = 'inches'

        else:
            print('Error: Invalid number or not a number for unit options. Please try again!')

    result = None

    while not result:
        user_grav_opt = input('Is the ball dropping on Earth? [y/n] ')

        if user_grav_opt == 'y':
            result = time_drop(user_height_meters)

        elif user_grav_opt == 'n':
            user_gravity = float(input('What is the value of the gravity, in meters per seconds squared? '))
            result = time_drop(user_height_meters,gravity=user_gravity)

        else:
            print('Error: Invalid input. Only enter "y" or "n". Please try again!')

    print('')
    print(f'The time it takes a ball dropped from {user_height} {units} to reach the ground is {result:.2f} seconds.')
