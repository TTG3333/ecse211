#!/usr/bin/env python3

'''
    Main helper used for driving.

    Before using, please use wait_ready_sensors in another file.
'''

from time           import sleep
from utils.dnoise   import dNoise

# ---------------------------------------------------- #
# Configurable settings

## Speed Configurations
BASE_SPEED      = 100
ADJUST_SPEED    = 30

## Color Configurations
WHITE_CONSTANT = 255
BLACK_CONSTANT = 18

TURNING_THRESHOLD = (WHITE_CONSTANT + BLACK_CONSTANT) / 2 - 20
TURNING_THRESHOLD_TOLERANCE = 20

## Polling Configurations
POLLING_SPEED = 0.02

## Certainty Behavior
COLOR_CERTAINTY = True

## dNoise Derivative Behavior
MAX_SLOPE = 20

# #################### #
# ---------------------------------------------------- #

global US_SENSOR, COLOR_SENSOR, LEFT_MOTOR, RIGHT_MOTOR

# Configurable settings
def _drive_straight(multiplier=1):
    LEFT_MOTOR  .set_dps(-BASE_SPEED * multiplier)
    RIGHT_MOTOR .set_dps(-BASE_SPEED * multiplier)

def _drive_offset(offset=0):
    LEFT_MOTOR  .set_dps(-BASE_SPEED + offset)
    RIGHT_MOTOR .set_dps(-BASE_SPEED - offset)

def follow_line(distance=5):
    noiser = dNoise(MAX_SLOPE)

    while True:
        lum = sum(COLOR_SENSOR.get_rgb()) / 3

        if lum < TURNING_THRESHOLD - TURNING_THRESHOLD_TOLERANCE:
            _drive_offset(ADJUST_SPEED)
        elif lum > TURNING_THRESHOLD + TURNING_THRESHOLD_TOLERANCE:
            _drive_offset(ADJUST_SPEED * -1)
        else:
            _drive_straight()

        if noiser.add(US_SENSOR.get_value()):
            if noiser.get() < distance:
                break

        sleep(POLLING_SPEED)

# -- Wrappers ----------------------
def stop():
    _drive_straight(0)

def drive_back():
    _drive_straight(-1)