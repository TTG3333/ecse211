#!/usr/bin/env python3

'''
    Main helper used for driving.

    Before using, please use wait_ready_sensors in another file.
'''

from time           import sleep
from utils.color    import Color
from utils.dnoise   import dNoise

# ---------------------------------------------------- #
# Configurable settings

## Speed Configurations
BASE_SPEED      = 300
ADJUST_SPEED    = 100

## Color Configurations
WHITE_CONSTANT = 255
BLACK_CONSTANT = 18

TURNING_THRESHOLD = (WHITE_CONSTANT + BLACK_CONSTANT) / 2 - 10
TURNING_THRESHOLD_TOLERANCE = 20

## Polling Configurations
POLLING_SPEED = 0.02

## Certainty Behavior
COLOR_CERTAINTY = True

## dNoise Derivative Behavior
MAX_SLOPE = 20

# ---------------------------------------------------- #

def init_d(color, gyro, ultrasonic, right_m, left_m):
    global GYRO_SENSOR, COLOR_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR
    GYRO_SENSOR = gyro
    COLOR_SENSOR = color
    US_SENSOR = ultrasonic
    LEFT_MOTOR = left_m
    RIGHT_MOTOR = right_m

# ---------------------------------------------------- #

def _drive_straight(multiplier=1):
    LEFT_MOTOR  .set_dps(-BASE_SPEED * multiplier)
    RIGHT_MOTOR .set_dps(-BASE_SPEED * multiplier)

def _drive_offset(offset=0):
    LEFT_MOTOR  .set_dps(-BASE_SPEED + offset)
    RIGHT_MOTOR .set_dps(-BASE_SPEED - offset)

# ---------------------------------------------------- #

def drive_straight(until_distance=None, until_colors=None, delay=None):
    noiser = dNoise(MAX_SLOPE)
    _drive_straight()

    while True:
        if until_colors:
            color = Color(*COLOR_SENSOR.get_rgb())
            if str(color) in until_colors:
                if not COLOR_CERTAINTY or color.is_certain():
                    break

        if until_distance is not None:
            if noiser.add(US_SENSOR.get_value()):
                if noiser.get() < until_distance:
                    break

        sleep(POLLING_SPEED)

    if delay:
        sleep(delay)

    stop()

def follow_line(until_distance=8, until_colors=None, delay=None):
    noiser = dNoise(MAX_SLOPE)

    while True:
        lum = sum(COLOR_SENSOR.get_rgb()) / 3
        error = lum - TURNING_THRESHOLD

        max_range = TURNING_THRESHOLD_TOLERANCE
        normalized = max(-1, min(1, error / max_range))
        offset = normalized * ADJUST_SPEED

        _drive_offset(offset)

        if noiser.add(US_SENSOR.get_value()):
            print(noiser.get(), until_distance)
            if noiser.get() < until_distance:
                break

        if until_colors:
            color = Color(*COLOR_SENSOR.get_rgb())
            if str(color) in until_colors:
                if not COLOR_CERTAINTY or color.is_certain():
                    break

        sleep(POLLING_SPEED)

    if delay:
        sleep(delay)

    stop()

# -- Wrappers ----------------------
def stop():
    _drive_straight(0)

def drive_back():
    _drive_straight(-1)