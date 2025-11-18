#!/usr/bin/env python3

"""
Testing of the gyro sensor
"""
 
from utils import sound
from utils.brick import Motor, EV3GyroSensor, wait_ready_sensors
from time import sleep
import line_follower
import package_delivery

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
GYRO_SENSOR = EV3GyroSensor(4)
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

# adjust this if you want
OVERSHOOT_UNDERSHOOT = 3

def turn_90_deg(direction: str):
    i = 1 if direction.lower() == "left" else -1 if direction.lower() == "right" else 0
    offset = GYRO_SENSOR.get_abs_measure()

    LEFT_MOTOR.set_dps(200 * int(i))
    RIGHT_MOTOR.set_dps(-200 * int(i))
    while abs((GYRO_SENSOR.get_abs_measure() - offset)) < 90 - (OVERSHOOT_UNDERSHOOT * i):
        print("current degrees turned: " + str(GYRO_SENSOR.get_abs_measure() - offset))
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

def turn_180_deg():
    offset = GYRO_SENSOR.get_abs_measure()
    
    LEFT_MOTOR.set_dps(-200)
    RIGHT_MOTOR.set_dps(200)
    while abs((GYRO_SENSOR.get_abs_measure() - offset)) < 180 - OVERSHOOT_UNDERSHOOT:
        print("current degrees turned: " + str(GYRO_SENSOR.get_abs_measure() - offset))
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

