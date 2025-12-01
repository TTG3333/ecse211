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
ADJUST_SPEED    = 50

## Color Configurations
WHITE_CONSTANT = 255
BLACK_CONSTANT = 18

TURNING_THRESHOLD = (WHITE_CONSTANT + BLACK_CONSTANT) / 2 - 10
TURNING_THRESHOLD_TOLERANCE = 20

## Polling Configurations
POLLING_SPEED = 0.02

## Certainty Behavior
COLOR_CERTAINTY = True

## Adaptive Speed
DISTANCE_ERROR = 5
ADAPTIVE_PERCENT = 0.25

## dNoise Derivative Behavior
MAX_SLOPE = 40

# ---------------------------------------------------- #

def init_d(color, gyro, ultrasonic, right_m, left_m, package_m):
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

def _drive_offset(offset=0, multiplier=1):
    LEFT_MOTOR  .set_dps((-BASE_SPEED + offset) * multiplier)
    RIGHT_MOTOR .set_dps((-BASE_SPEED - offset) * multiplier)

# ---------------------------------------------------- #

def stop_moving():
    LEFT_MOTOR  .set_dps(0)
    RIGHT_MOTOR .set_dps(0)

# ---------------------------------------------------- #

def drive_straight(
        until_distance=None, until_colors=None, delay=None, 
        backwards=False, speed_multiplier=1, adaptive_speed=True
):
    noiser = dNoise(MAX_SLOPE)
    noiser.add(US_SENSOR.get_value())
    mult = 1 if not backwards else -1
    
    _drive_straight(speed_multiplier * mult)

    while True:
        if until_colors:
            color = Color(*COLOR_SENSOR.get_rgb())
            if str(color) in until_colors:
                if not COLOR_CERTAINTY or color.is_certain():
                    break

        if until_distance is not None:
            if noiser.add(US_SENSOR.get_value()):
                print("Added")
                if (not backwards and noiser.get() < until_distance) or (backwards and noiser.get() > until_distance):
                    break
                
                if adaptive_speed:
                    if not backwards:
                        diff = noiser.get() - until_distance
                    else:
                        diff = until_distance - noiser.get()

                    diff = max(diff, 0)
                    ratio = min(diff / DISTANCE_ERROR, 1.0)
                    factor = ADAPTIVE_PERCENT + (1.0 - ADAPTIVE_PERCENT) * ratio
                    print(diff, factor)

                    _drive_straight(speed_multiplier * mult * factor)
            else:
                print(f"Rejected value {US_SENSOR.get_value()}")


        sleep(POLLING_SPEED)

    if delay:
        sleep(delay)

    stop()

    if not delay:
        return noiser.get() if until_distance is not None else None, color if until_colors else None
    else:
        return None, None

def follow_line(
        until_distance=8, until_colors=None, delay=None, 
        speed_multiplier=1, adaptive_speed=True
):
    noiser = dNoise(MAX_SLOPE)
    noiser.add(US_SENSOR.get_value())

    while True:
        lum = sum(COLOR_SENSOR.get_rgb()) / 3
        error = lum - TURNING_THRESHOLD

        max_range = TURNING_THRESHOLD_TOLERANCE
        normalized = max(-1, min(1, error / max_range))
        offset = ADJUST_SPEED * normalized

        _drive_offset(offset, speed_multiplier)

        if noiser.add(US_SENSOR.get_value()):
            if noiser.get() < until_distance:
                break

            if adaptive_speed:
                    diff = abs(noiser.get() - until_distance)
                    ratio = diff / DISTANCE_ERROR
                    if ratio < 1:
                        factor = ADAPTIVE_PERCENT + (1.0 - ADAPTIVE_PERCENT) * ratio
                        _drive_straight(speed_multiplier * factor)

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

def drive_back(multiplier=1):
    _drive_straight(-multiplier)

def drive_distance(distance, until_colors=None, delay=None, backwards=False, speed_multiplier=1, adaptive_speed=True):
    current_distance = US_SENSOR.get_value()
    target_distance = current_distance - distance if not backwards else current_distance + distance
    dist, color = drive_straight(until_distance=target_distance, until_colors=until_colors, delay=delay, backwards=backwards, speed_multiplier=speed_multiplier, adaptive_speed=adaptive_speed)
    return abs(current_distance - dist), color
