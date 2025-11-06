#!/usr/bin/env python3

"""
Testing of the gyro sensor
"""
 
from utils import sound
from utils.brick import EV3GyroSensor, wait_ready_sensors

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
GYRO_SENSOR = EV3GyroSensor(3)

wait_ready_sensors() 


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


if __name__=='__main__':
    while True:
        input("lol")
        print(GYRO_SENSOR.get_abs_measure())
    
