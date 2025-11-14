#!/usr/bin/env python3

"""
Testing of the gyro sensor
"""
 
from utils import sound
from utils.brick import Motor, EV3GyroSensor, wait_ready_sensors

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
GYRO_SENSOR = EV3GyroSensor(4)
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

wait_ready_sensors() 


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


if __name__=='__main__':
    GYRO_SENSOR.set_mode('abs')
    offset = 0
    while True:
        i = input("input: ")
        if i == 'r':
            offset = GYRO_SENSOR.get_abs_measure()
            print("measure reset")
        elif i == '1' or i == '-1':
            offset = GYRO_SENSOR.get_abs_measure()
            LEFT_MOTOR.set_dps(200 * int(i))
            RIGHT_MOTOR.set_dps(-200 * int(i))
            while abs((GYRO_SENSOR.get_abs_measure() - offset)) < 90:
                print("current degrees turned: " + str(GYRO_SENSOR.get_abs_measure() - offset))
            LEFT_MOTOR.set_dps(0)
            RIGHT_MOTOR.set_dps(0)
        else:
            print("adjusted gyro sensor value read: " + str(GYRO_SENSOR.get_abs_measure() - offset))
        
