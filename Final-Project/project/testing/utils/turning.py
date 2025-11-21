#!/usr/bin/env python3

'''
    Main helper used for turning.
    Provides useful functions for turning.

    Before using, please use wait_ready_sensors in another file.
'''

from time           import sleep, monotonic
from utils.color    import Color

# ---------------------------------------------------- #
# Configurable settings

## Turning Configurations
TURN_SPEED = 100

## Polling Configurations
POLLING_SPEED = 0.02

## Certainty Behavior
COLOR_CERTAINTY = True

# ---------------------------------------------------- #

def init_t(color, gyro, ultrasonic, right_m, left_m):
    global GYRO_SENSOR, COLOR_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR
    GYRO_SENSOR = gyro
    COLOR_SENSOR = color
    US_SENSOR = ultrasonic
    LEFT_MOTOR = left_m
    RIGHT_MOTOR = right_m

# ---------------------------------------------------- #

def _get_rotation():
    return GYRO_SENSOR.get_abs_measure()

def _begin_turn(multiplier=1):
    LEFT_MOTOR  .set_dps(TURN_SPEED * multiplier * -1)
    RIGHT_MOTOR .set_dps(TURN_SPEED * multiplier)

# ---------------------------------------------------- #

def turn_angle(deg, direction='left', until_colors=None, after_dt=0):
    t0 = monotonic()
    offset = _get_rotation()
    i = 1 if direction.lower() == "left" else -1
    _begin_turn(i)

    while True:
        if (monotonic() - t0) > after_dt:
            current = abs(_get_rotation() - offset)
            if current > deg:
                break
            
            if until_colors:
                color = Color(*COLOR_SENSOR.get_rgb())
                if str(color) in until_colors and (not COLOR_CERTAINTY or color.is_certain()):
                    break

        sleep(POLLING_SPEED)

    stop()

# -- Wrappers ----------------------
def turn_90_deg(direction='left'):
    turn_angle(90, direction)

def turn_180_deg(direction='left'):
    turn_angle(180, direction)

def turn_until(direction='left', until_colors=None, after_dt=0):
    turn_angle(360, direction, after_dt)

def stop():
    _begin_turn(0)