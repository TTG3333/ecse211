#!/usr/bin/env python3

"""
Testing of the colors found on the playing field
"""
 
import time
from scipy.stats import circmean, circvar
from utils.brick import wait_ready_sensors, EV3ColorSensor
from utils.color import Color

C_SENSOR = EV3ColorSensor(1)
wait_ready_sensors()

if __name__=='__main__':

    def mean(vals):
        return sum(vals) / len(vals)
    
    def var(vals):
        m = mean(vals)
        return sum((x - m) ** 2 for x in values) / len(values)
    
    list = []
    time.sleep(1)
    for i in range(0, 60):
        r,g,b = C_SENSOR.get_rgb()
        color = Color(r,g,b)
        list.append(color)
        time.sleep(0.1)

    # Find the highest and lowest value
    values = [c.value for c in list]
    print(f"(VALUES) Max: {max(values)}, Min: {min(values)}, Avg: {circmean(values)}, Var: {circvar(values)}")

    # Find the highest saturation
    saturations = [c.saturation for c in list]
    print(f"(SATURATION) Max: {max(saturations)}, Min: {min(saturations)}, Avg: {circmean(saturations)}, Var: {circvar(saturations)}")

    # Find the highest hue
    hues = [c.hue for c in list]
    print(f"(HUES) Max: {max(hues)}, Min: {min(hues)}, Avg: {circmean(hues)}, Var: {circvar(hues)}")