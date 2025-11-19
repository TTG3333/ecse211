from utils.brick import Motor, wait_ready_sensors, SensorError, EV3GyroSensor, EV3ColorSensor, EV3UltrasonicSensor
from math import pi, tan, sqrt, atan
from utils.color import Color
from package_delivery import move_to_next as deliver_package
import time


C_SENSOR = EV3ColorSensor(1)
US_SENSOR = EV3UltrasonicSensor(3)
GYRO_SENSOR = EV3GyroSensor(4)

LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

LEFT_MOTOR.reset_encoder()
RIGHT_MOTOR.reset_encoder()

BASE_SPEED = -200
TURN_SPEED = 200
SENSOR_POLL_SLEEP = 0.05

HALF_WALL = 12  # in cm

def distance_to_wall(deg): # in cm
    if deg < atan(2) * 180 / pi:
        return HALF_WALL * sqrt(1 + tan(pi * deg / 180)**2)
    elif deg < 180 - atan(2) * 180 / pi:
        return 2*HALF_WALL * sqrt(1 + tan(pi * abs(90-deg) / 180)**2)
    else:
        return HALF_WALL * sqrt(1 + tan(pi * (180 - deg) / 180)**2)

def get_current_color():
    r, g, b = C_SENSOR.get_rgb()
    return str(Color(r, g, b)).lower()

def run_until_distance(dist, direction='forward', color=['yellow']):
    direction = 1 if direction.lower() == 'forward' else -1
    start_distance = US_SENSOR.get_value()
    LEFT_MOTOR.set_dps(BASE_SPEED*direction)
    RIGHT_MOTOR.set_dps(BASE_SPEED*direction)
    while True:
        current_distance = US_SENSOR.get_value()
        if abs(start_distance - current_distance) >= dist:
            LEFT_MOTOR.set_dps(0)
            RIGHT_MOTOR.set_dps(0)
            return abs(start_distance - current_distance)
        if color:
            if not get_current_color() in color:
                LEFT_MOTOR.set_dps(0)
                RIGHT_MOTOR.set_dps(0)
                return abs(start_distance - current_distance)
        time.sleep(SENSOR_POLL_SLEEP)

def turn_angle(deg, direction='left'):
    i = 1 if direction.lower() == "left" else -1
    offset = GYRO_SENSOR.get_abs_measure()

    LEFT_MOTOR.set_dps(TURN_SPEED * i)
    RIGHT_MOTOR.set_dps(-TURN_SPEED * i)
    while abs((GYRO_SENSOR.get_abs_measure() - offset)) < abs(deg):
        pass
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)

def run():
    run_until_distance(4, direction='forward', color=["organge"])
    if get_current_color() == 'red':
        print("Restricted room detected, backing up.")
        run_until_distance(4, direction='backward', color=["red"])
        return
    zero = GYRO_SENSOR.get_abs_measure()
    # Start at -25, end at 25
    for angle in range(-25, 30, 5):
        turn_angle(angle - (GYRO_SENSOR.get_abs_measure() - zero), direction='left' if angle - (GYRO_SENSOR.get_abs_measure() - zero) > 0 else 'right')
        dist = distance_to_wall(90 + angle)
        print(f"Angle: {angle}, Distance to wall: {dist} cm")
        # The square is at least 2 inches away from the wall
        travelled = run_until_distance(dist - 5, direction='forward', color=["yellow", "orange"])
        if get_current_color() == "green":
            print("Green square detected, delivering package.")
            travelled2 = run_until_distance(8, direction="backward", color=[])
            deliver_package()
            run_until_distance(abs(travelled - travelled2), direction="forward" if travelled < travelled2 else "backward", color=[])
            angle = -angle
            turn_angle(angle - (GYRO_SENSOR.get_abs_measure() - zero), direction='left' if angle - (GYRO_SENSOR.get_abs_measure() - zero) > 0 else 'right')
            return
        run_until_distance(travelled, direction='backward', color=["yellow", get_current_color()])

if __name__ == '__main__':
    wait_ready_sensors()
    run()