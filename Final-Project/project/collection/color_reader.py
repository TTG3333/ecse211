#!/usr/bin/env python3

"""
Testing of the colors found on the playing field
"""
 
import time
from utils.brick import wait_ready_sensors, EV3ColorSensor
from utils.color import Color

C_SENSOR = EV3ColorSensor(1)
wait_ready_sensors()

if __name__=='__main__':
    time.sleep(1)
    while True:
        r,g,b = C_SENSOR.get_rgb()
        color = Color(r,g,b)
        print(str(color))
        time.sleep(0.25)