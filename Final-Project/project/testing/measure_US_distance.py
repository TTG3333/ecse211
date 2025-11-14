#!/usr/bin/env python3

from utils.brick import wait_ready_sensors, EV3UltrasonicSensor
from time import sleep

US_SENSOR = EV3UltrasonicSensor(3)

if __name__ == "__main__":
    wait_ready_sensors()
    while True:
        print(US_SENSOR.get_value())
        sleep(0.1)
