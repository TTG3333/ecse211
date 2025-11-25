from utils.brick import Motor, wait_ready_sensors, SensorError, EV3GyroSensor, EV3ColorSensor, EV3UltrasonicSensor
from math import pi, tan, sqrt, atan
from utils.color import Color
from package_delivery import move_to_next as deliver_package
from utils.sounds import play_collect, play_help
import time
import threading

from utils.turning import turn_angle

COLOR_SENSOR = EV3ColorSensor(1)
US_SENSOR = EV3UltrasonicSensor(3)
GYRO_SENSOR = EV3GyroSensor(4)

LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

LEFT_MOTOR.reset_encoder()
RIGHT_MOTOR.reset_encoder()

BASE_SPEED = -100
TURN_SPEED = 100
SENSOR_POLL_SLEEP = 0.05

QUICK_POLL_TIME = 0.02
US_SENSOR_VALS = [None] * 10
STOP = False

COLOR_THRESHOLD = 0.7

TOLERANCE = 0.5  # in cm
HALF_WALL = 12  # in cm
WHEEL_CIRCUMFERENCE = 4 * pi # in cm

def us_sensor_handler():
    global US_SENSOR_VALS
    index = 0
    while True:
        if STOP:
            return
        val = US_SENSOR.get_value()
        if val is not None:
            US_SENSOR_VALS[index] = val
            index = (index + 1) % len(US_SENSOR_VALS)
        time.sleep(QUICK_POLL_TIME)

def distance_to_wall(deg): # in cm
    if deg < atan(2) * 180 / pi:
        return HALF_WALL * sqrt(1 + tan(pi * deg / 180)**2)
    elif deg < 180 - atan(2) * 180 / pi:
        return 2*HALF_WALL * sqrt(1 + tan(pi * abs(90-deg) / 180)**2)
    else:
        return HALF_WALL * sqrt(1 + tan(pi * (180 - deg) / 180)**2)

def get_current_color(certainty=False):
    unsure = []
    delay = 0.02
    for _ in range(5):
        r, g, b = COLOR_SENSOR.get_rgb()
        if None in [r, g, b]:
            time.sleep(delay)
            delay *= 2 # Exponential backoff
            continue
        color = Color(r, g, b)
        if color.predict()[1] >= 0.7:
            return color.predict()[0] if not certainty else color.predict()
        else:
            unsure.append(color.predict())
            time.sleep(SENSOR_POLL_SLEEP/5)
    if unsure:
        unsure.sort(key=lambda x: x[1], reverse=True)
        return unsure[0][0] if not certainty else unsure[0]
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)
    play_help()
    raise SensorError("Unable to read from colour sensor")

def get_us_sensor(): # Gets the median value
    vals = [v for v in US_SENSOR_VALS if v is not None]
    return sorted(vals)[len(vals)//2] if vals else None

def old_get_us_sensor():
    for _ in range(5):
        val = US_SENSOR.get_value()
        if val is not None:
            return val
        time.sleep(SENSOR_POLL_SLEEP/5)
    raise SensorError("Unable to read from ultrasonic sensor")

def run_until_distance(dist, direction='forward', color=['Yellow']):
    direction = 1 if direction.lower() == 'forward' else -1
    start_distance = get_us_sensor()
    print(f"Moving {dist} cm, starting sensor value {start_distance} cm")
    # total_time = (dist/WHEEL_CIRCUMFERENCE) * 360 / abs(BASE_SPEED)
    # start_time = time.time()
    LEFT_MOTOR.set_dps(BASE_SPEED*direction)
    RIGHT_MOTOR.set_dps(BASE_SPEED*direction)
    while True:
        current_distance = get_us_sensor()
        if abs(start_distance - current_distance) >= dist + TOLERANCE:
        # if time.time() - start_time >= total_time:
            LEFT_MOTOR.set_dps(0)
            RIGHT_MOTOR.set_dps(0)
            # stop_time = time.time()
            # print(f"Existed at time {stop_time - start_time} seconds")
            # return (stop_time - start_time) * abs(BASE_SPEED) / 360 * WHEEL_CIRCUMFERENCE
            print(f"Exited at distance {abs(start_distance - current_distance)} cm")
            return (abs(start_distance - current_distance), None)
        if color:
            c, cert = get_current_color(True)
            if cert >= COLOR_THRESHOLD and c not in color:
                LEFT_MOTOR.set_dps(0)
                RIGHT_MOTOR.set_dps(0)
                # stop_time = time.time()
                print(f"Exited at color {c}")
                return (abs(start_distance - current_distance), c)
                # return (stop_time - start_time) * abs(BASE_SPEED) / 360 * WHEEL_CIRCUMFERENCE
        time.sleep(SENSOR_POLL_SLEEP)

def run():
    delivered = False
    traveled, color = run_until_distance(5, direction='forward', color=["Orange", "Black"])
    if color == 'Red':
        print("Restricted room detected, backing up.")
        turn_angle(270, direction='right', colors=["Black"])
        return delivered
    zero = GYRO_SENSOR.get_abs_measure()
    print(f"Entered room, starting scan from angle {zero} degrees.")
    # Start at -30, end at 30, sensor is clockwise
    for angle in range(-30, 35, 5):
        print()
        print(f"Currently at {GYRO_SENSOR.get_abs_measure() - zero}, going to {angle}")
        turn_angle(angle - (GYRO_SENSOR.get_abs_measure() - zero), direction='left' if angle - (GYRO_SENSOR.get_abs_measure() - zero) < 0 else 'right')
        dist = distance_to_wall(90 + angle)
        print(f"Angle: {angle}, Distance to wall: {dist} cm")
        # The square is at least 2 inches away from the wall
        traveled, color = run_until_distance(dist - 7, direction='forward', color=["Yellow", "Orange"])
        if color == "Green":
            print("Green square detected, delivering package.")
            traveled2, _ = run_until_distance(8, direction="backward", color=[])
            deliver_package()
            play_collect().wait_done()
            run_until_distance(8, direction="forward", color=["Orange", "Yellow", "White", "Black"])
            run_until_distance(traveled, direction="backward", color=["Yellow", "Green"])
            break
        run_until_distance(traveled, direction='backward', color=["Yellow", "Green", color])
    # Exit facing on the black line, overshoot to the left of the line
    run_until_distance(0.75, direction="backward", color=["Yellow"])
    turn_angle(270, direction='right', colors=["Black"])
    return delivered

if __name__ == '__main__':
    wait_ready_sensors()
    time.sleep(0.5)
    t = threading.Thread(target=us_sensor_handler)
    t.start()
    time.sleep(1)
    try:
        run()
    except Exception as e:
        STOP = True
        print(f"{e.__class__.__name__}: {e}")
        from sys import exit
        exit()
    STOP = True
