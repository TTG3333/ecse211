#!/usr/bin/env python3

"""
Testing of the colors found on the playing field
"""
 
from utils.brick import wait_ready_sensors, EV3ColorSensor
from utils.color import Color

C_SENSOR = EV3ColorSensor(1)
wait_ready_sensors()

if __name__=='__main__':
    list = []
    for i in range(0,200):
        r,g,b = C_SENSOR.get_rgb()
        color = Color(r,g,b)
        list.append(color)

    # Find the highest and lowest value
    values = [c.value for c in list]
    print(f"(VALUES) Max: {max(values)}, Min: {min(values)}")

    # Find the highest saturation
    saturations = [c.saturation for c in list]
    print(f"(SATURATION) Max: {max(saturations)}, Min: {min(saturations)}")

    # Find the highest hue
    hues = [c.hue for c in list]
    print(f"(HUES) Max: {max(hues)}, Min: {min(hues)}")