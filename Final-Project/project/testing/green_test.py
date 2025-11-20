from utils.brick import Motor, wait_ready_sensors, SensorError, EV3GyroSensor, EV3ColorSensor, EV3UltrasonicSensor
from math import pi, tan, sqrt, atan
from utils.color import Color
from package_delivery import move_to_next as deliver_package
from sounds import play_collect, play_help
import time
import threading

C_SENSOR = EV3ColorSensor(1)


def get_current_color(certainty=False):
    unsure = []
    delay = 0.02
    for _ in range(5):
        r, g, b = C_SENSOR.get_rgb()
        if None in [r, g, b]:
            time.sleep(delay)
            delay *= 2 # Exponential backoff
            continue
        color = Color(r, g, b)
        if color.predict()[1] >= 0.7:
            return color.predict()[0].lower() if not certainty else (color.predict()[0].lower(), color.predict()[1])
        else:
            unsure.append(color.predict())
            time.sleep(0.01/5)
    if unsure:
        unsure.sort(key=lambda x: x[1], reverse=True)
        return unsure[0][0].lower() if not certainty else (unsure[0][0].lower(), unsure[0][1])
    # LEFT_MOTOR.set_dps(0)
    # RIGHT_MOTOR.set_dps(0)
    play_help()
    raise SensorError("Unable to read from colour sensor")

while True:
    if get_current_color() == "green":
        play_collect.wait_done()
        break
    time.sleep(0.05)