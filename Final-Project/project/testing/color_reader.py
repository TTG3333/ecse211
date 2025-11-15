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

def log(label):
    r,g,b = C_SENSOR.get_rgb()

    color = Color(r,g,b)
    predicted = str(color)

    label = input(f"What color is expected? (Predicted: {predicted}): ")
    if label == "":
        label = predicted

    print(f"Added: ({r,g,b}) as {label}")
    with open("../collection/color_data.csv", "a", newline="\n") as file:
        writer = csv.writer(file)
        writer.writerow([r, g, b, label])

if __name__=='__main__':
    time.sleep(1)
    while True:
        if BUTTON.is_pressed():
            log()
            time.sleep(1)
        time.sleep(0.1)