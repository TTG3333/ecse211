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
    i = 0
    while True:
        r,g,b = COLOR_SENSOR.get_rgb()
        color = Color(r,g,b)
        print(f"{i} - Predicted color: \033[38;2;{r};{g};{b}m{color.predict()}\033[0m, RGB: {r,g,b}, Saturation: {color.saturation}, Value: {color.value}")
        time.sleep(0.25)
