#!/usr/bin/env python3

'''
    Main helper used for turning.
    Provides useful functions for turning.
'''

from utils.color import Color

# Configurable settings

TURN_SPEED = 100

# #################### #

global LEFT_MOTOR, RIGHT_MOTOR, GYRO_SENSOR, COLOR_SENSOR

def get_rotation():
    GYRO_SENSOR.get_abs_measure()

def turn_angle(deg, direction='left', colors=None):
    if not colors:
        colors = []

    offset = get_rotation()
    i = 1 if direction.lower() == "left" else -1
   
    LEFT_MOTOR  .set_dps(TURN_SPEED * i)
    RIGHT_MOTOR .set_dps(TURN_SPEED * i * -1)

    while True:
        current = abs(get_rotation() - offset)
        if current > deg:
            break
        
        if colors:
            color = Color(*COLOR_SENSOR.get_rgb())
            if str(color) in colors:
                break

    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

# -- Wrappers ----------------------
def turn_90_deg(direction='left'):
    turn_angle(90, direction)

def turn_180_deg(direction='left'):
    turn_angle(180, direction)

def turn_until(direction='left', colors=None):
    turn_angle(360, direction, colors)