#!/usr/bin/env python3

"""
Testing of the colors found on the playing field
"""
 
import time
from utils.brick import wait_ready_sensors, EV3ColorSensor
from utils.color import Color

COLOR_SENSOR = EV3ColorSensor(1)
wait_ready_sensors()

if __name__=='__main__':
    time.sleep(1)
    while True:
        r,g,b = COLOR_SENSOR.get_rgb()
        color = Color(r,g,b)
        print(color.predict())
        time.sleep(0.25)