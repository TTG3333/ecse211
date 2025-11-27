#!/usr/bin/env python3

'''
    Main helper used for the intra-room subsystem.
    Provides useful functions for scanning in a room.

    Before using, please use wait_ready_sensors in another file.
'''

from utils.color    import Color
from utils.sounds   import play_collect
from utils.driver   import drive_distance, drive_straight
from utils.turning  import turn_angle
from time           import sleep
from math           import pi, sqrt, tan, atan

# ---------------------------------------------------- #
# Configurable settings

# Turning Configurations
START_ANGLE = -30
END_ANGLE   = 30
ANGLE_STEP  = 5

# Certainty Behavior
COLOR_CERTAINTY = True

# Measurements, all in cm
BELT_CIRCUMFERENCE = 3.5 * pi
DISTANCE_PER_CUBE = 2.5 + 0.8
HALF_WALL = 12

# Motor speeds, in dps
BASE_SPEED = -100
TURN_SPEED = 100

# ---------------------------------------------------- #

def init_r(color, gyro, ultrasonic, right_m, left_m, package_m):
    global GYRO_SENSOR, COLOR_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR, PACKAGE_MOTOR
    GYRO_SENSOR = gyro
    COLOR_SENSOR = color
    US_SENSOR = ultrasonic
    LEFT_MOTOR = left_m
    RIGHT_MOTOR = right_m
    PACKAGE_MOTOR = package_m

# ---------------------------------------------------- #

def _deliver_package():
    # Calculate the number of degrees to turn
    degrees = DISTANCE_PER_CUBE / BELT_CIRCUMFERENCE * 360

    # Move the belt motor
    PACKAGE_MOTOR.set_limits(dps=90)
    PACKAGE_MOTOR.set_position_relative(-degrees)
    sleep(degrees/90 + 0.25)  # Wait for the movement to complete, the wait_is_stopped doesn't seem to work reliably

def _distance_to_wall(deg): # in cm
    if deg < atan(2) * 180 / pi:
        return HALF_WALL * sqrt(1 + tan(pi * deg / 180)**2)
    elif deg < 180 - atan(2) * 180 / pi:
        return 2*HALF_WALL * sqrt(1 + tan(pi * abs(90-deg) / 180)**2)
    else:
        return HALF_WALL * sqrt(1 + tan(pi * (180 - deg) / 180)**2)

# ---------------------------------------------------- #

def stop_room():
    PACKAGE_MOTOR.set_dps(0)

# ---------------------------------------------------- #

def handle_room():
    _, color = drive_distance(5, until_colors=["Red", "Yellow"])

    # If in a restricted room
    if not COLOR_CERTAINTY or color.is_certain():
        if str(color) == 'Red':
            print("Restricted room detected, backing up.")
            return False

    # Not in a restricted room
    zero = GYRO_SENSOR.get_abs_measure()
    print(f"Entered room, starting scan from angle {zero} degrees.")

    # Start at -30, end at 30, sensor is clockwise
    delivered = False
    for desired in range(START_ANGLE, END_ANGLE, ANGLE_STEP):
        current    = GYRO_SENSOR.get_abs_measure() - zero
        add        = desired - current
        print(f"\n Currently at {current}, going to {desired} by turning {add} degrees")

        turn_angle(abs(add), direction='left' if add < 0 else 'right')
        #dist = _distance_to_wall(90 + desired)

        # The square is at least 2 inches away from the wall
        _, color = drive_straight(None, until_colors=["White", "Green", "Black", "Blue"])

        # If green square detected
        if not COLOR_CERTAINTY or color.is_certain():
            print(color.predict())
            if str(color) == "Green":
                print("Found green! Delivering")
                delivered = True
                drive_distance(8, backwards=True)
                _deliver_package()
                play_collect().wait_done()
                drive_distance(8)

        drive_straight(None, backwards=True, until_colors=["Yellow"])
        drive_straight(None, backwards=True, until_colors=["Orange", "White", "Black"])
        if delivered:
            break
    
    offset = GYRO_SENSOR.get_abs_measure() - zero

    turn_angle(abs(offset), direction='right' if offset < 0 else 'left')

    return delivered