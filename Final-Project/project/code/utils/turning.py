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
TURN_SPEED = 300

## Polling Configurations
POLLING_SPEED = 0.02

## Certainty Behavior
COLOR_CERTAINTY = True

## Adaptive Speed
ANGLE_ERROR = 5
ADAPTIVE_PERCENT = 0.25

# ---------------------------------------------------- #

def init_t(color, gyro, ultrasonic, right_m, left_m, package_m):
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

def stop_turning():
    LEFT_MOTOR  .set_dps(0)
    RIGHT_MOTOR .set_dps(0)

# ---------------------------------------------------- #

def turn_angle(deg, direction='left', until_colors=None, after_dt=0, delay=None, adaptive_speed=True, angle_after_color=None):
    t0 = monotonic()
    offset = _get_rotation()
    i = 1 if direction.lower() == "left" else -1
    _begin_turn(i)

    while True:
        if (monotonic() - t0) > after_dt:
            current = abs(_get_rotation() - offset)
            if current > deg:
                break

            if adaptive_speed:
                diff = abs(current - deg)
                ratio = diff / ANGLE_ERROR
                if ratio < 1:
                    factor = ADAPTIVE_PERCENT + (1.0 - ADAPTIVE_PERCENT) * ratio
                    _begin_turn(i * factor)
            
            if until_colors:
                color = Color(*COLOR_SENSOR.get_rgb())
                if str(color) in until_colors and (not COLOR_CERTAINTY or color.is_certain()):
                    if angle_after_color:
                        until_colors = [] # Reset array for future checks
                        deg = current + angle_after_color
                    else:
                        break

        sleep(POLLING_SPEED)

    if delay:
        sleep(delay)

    stop()

# -- Wrappers ----------------------
def turn_90_deg(direction='left'):
    turn_angle(90, direction)

def turn_180_deg(direction='left'):
    turn_angle(180, direction)

def turn_until(direction='left', until_colors=None, after_dt=0, delay=None, adaptive_speed=None, max_angle=360, angle_after_color=None):
    turn_angle(max_angle, direction, until_colors, after_dt, delay, adaptive_speed, angle_after_color)

def turn_until_combined(direction='left', colors_list=None, after_dt=0, delay=None, adaptive_speed=None, max_angle=360):
    for colors in colors_list:
        turn_until(direction, until_colors=colors, after_dt=after_dt, delay=delay, adaptive_speed=adaptive_speed, max_angle=max_angle)

def stop():
    _begin_turn(0)