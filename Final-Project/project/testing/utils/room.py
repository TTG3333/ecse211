#!/usr/bin/env python3

'''
    Main helper used for the intra-room subsystem.
    Provides useful functions for scanning in a room.

    Before using, please use wait_ready_sensors in another file.
'''

from utils.color    import Color
from utils.sounds   import play_collect
from utils.driver   import drive_distance
from utils.turning  import turn_angle
from time           import sleep
from math           import pi, sqrt, tan, atan

# ---------------------------------------------------- #
# Configurable settings

# Turning Configurations
START_ANGLE = -30
END_ANGLE   = 35
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
    # Calculate the number of degres to turn
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

def handle_room():
    delivered = False
    _, color = drive_distance(5, until_colors=["Red", "Yellow"])

    # If in a restricted room
    if color == 'Red':
        print("Restricted room detected, backing up.")
        turn_angle(270, direction='right', until_colors=["Black"])
        return delivered

    # Not in a restricted room
    zero = GYRO_SENSOR.get_abs_measure()
    print(f"Entered room, starting scan from angle {zero} degrees.")

    # Start at -30, end at 30, sensor is clockwise
    for angle in range(START_ANGLE, END_ANGLE, ANGLE_STEP):
        print()
        print(f"Currently at {GYRO_SENSOR.get_abs_measure() - zero}, going to {angle} by turning {angle - (GYRO_SENSOR.get_abs_measure() - zero)} degrees")
        turn_angle(angle - (GYRO_SENSOR.get_abs_measure() - zero), direction='left' if angle - (GYRO_SENSOR.get_abs_measure() - zero) < 0 else 'right')
        dist = _distance_to_wall(90 + angle)
        print(f"Angle: {angle}, Distance to wall: {dist} cm")
        # The square is at least 2 inches away from the wall
        traveled, color = drive_distance(dist - 7, until_colors=["White", "Green", "Black", "Blue"])

        # If green square detected
        if color == "Green":
            delivered = True
            print("Green square detected, delivering package.")
            drive_distance(8, backwards=True)
            _deliver_package()
            play_collect().wait_done()
            drive_distance(8)
            drive_distance(traveled, backwards=True, until_colors=["Orange", "White", "Black"])
            break

        drive_distance(traveled, backwards=True, until_colors=["Orange", "White", "Black"])

    # Exit facing on the black line, overshoot to the left of the line
    drive_distance(0.75, backwards=True, until_colors=["White", "Black", "Orange"])
    turn_angle(270, direction='right', until_colors=["Black"])
    return delivered