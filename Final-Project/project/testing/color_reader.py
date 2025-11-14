#!/usr/bin/env python3

"""
Responsible for creating a dataset of colors on the map
"""
 
import time
import csv

from utils.brick import wait_ready_sensors, EV3ColorSensor, TouchSensor
from utils.color import Color

BUTTON = TouchSensor(2)
C_SENSOR = EV3ColorSensor(1)

wait_ready_sensors()

COLOR_LABEL = "White" # Change this before adding data

def log():
    r,g,b = C_SENSOR.get_rgb()
    print(f"Added: ({r,g,b}) as {COLOR_LABEL}")
    with open("../collection/color_data.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([r, g, b, COLOR_LABEL])

if __name__=='__main__':
    time.sleep(1)
    while True:
        if BUTTON.is_pressed():
            log()
            time.sleep(1)
        time.sleep(0.1)