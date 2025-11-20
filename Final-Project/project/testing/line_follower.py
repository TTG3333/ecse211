#  This current version works when the robot is initially placed on top of the black line, or slightly to the left.
#  If the robot was initially placed more to the right of the black line, it would drift away from the line.

from utils.brick import BP, Motor, wait_ready_sensors, SensorError, EV3UltrasonicSensor, EV3ColorSensor
import time
from math import pi
from package_delivery import move_to_next
from utils.color import Color
from noise_handler import NoiseEliminator
from utils.dnoise import dNoise

#  we should test the color sensor beforehand to see what values we get
#  for white, and black and use those
WHITE_SURFACE = 255  # all 3 values should be close to 255
BLACK_LINE = 18  # all 3 values should be close to 0
THRESHOLD = (WHITE_SURFACE + BLACK_LINE) / 2 - 20
TOLERANCE = 20

#  adjust speed if needed
BASE_SPEED = -200
TURNING_SPEED = -250

BACKUP_SPEED = 208

SENSOR_POLL_SLEEP = 0.02

# input correct ports
US_SENSOR = EV3UltrasonicSensor(3)
C_SENSOR = EV3ColorSensor(1)

# input correct motor ports
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

LEFT_MOTOR.reset_encoder()
RIGHT_MOTOR.reset_encoder()


def average_rgb_value(r, g, b):
    return (r + g + b) / 3


def drive_straight():
    LEFT_MOTOR.set_dps(BASE_SPEED)
    RIGHT_MOTOR.set_dps(BASE_SPEED)


def drive_slightly_left():
    LEFT_MOTOR.set_dps(BASE_SPEED + 25)
    RIGHT_MOTOR.set_dps(TURNING_SPEED - 25)


def drive_slightly_right():
    LEFT_MOTOR.set_dps(TURNING_SPEED)
    RIGHT_MOTOR.set_dps(BASE_SPEED)


def follow_line(rgb_average):
    #  drift slightly left if closer to black line
    if rgb_average < THRESHOLD - TOLERANCE:
        drive_slightly_left()
        current_dir = "LEFT"
        return current_dir
    #  get back to the black line
    elif rgb_average > THRESHOLD + TOLERANCE:
        drive_slightly_right()
        current_dir = "RIGHT"
        return current_dir
    else:
        drive_straight()
        current_dir = "STRAIGHT"
        return current_dir


def stop_robot():
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)


def backup():
    LEFT_MOTOR.set_dps(BACKUP_SPEED)
    RIGHT_MOTOR.set_dps(BACKUP_SPEED)
    time.sleep(1)
    stop_robot()


us_filter = dNoise(20, 2)
def run(until_what):
    current_dir = "LEFT"
    while True:
        try:
            r, g, b, lum = C_SENSOR.get_value()
            avg = average_rgb_value(r, g, b)

            # # stop on green square
            # if b < 25 and abs(r-b) > 10:
            #     stop_robot()
            #     backup()
            #     move_to_next()
            #     time.sleep(2)
            #     LEFT_MOTOR.set_dps(-BACKUP_SPEED)
            #     RIGHT_MOTOR.set_dps(-BACKUP_SPEED)
            #     time.sleep(1.5)
            #     if current_dir == "LEFT":
            #         drive_slightly_left()
            #     elif current_dir == "RIGHT":
            #         drive_slightly_right()
            #     else:
            #         drive_straight()

            # follow line
            current_dir = follow_line(avg)

            distance = US_SENSOR.get_value()
            print("Distance:", str(distance))
            print(f"Derivative: {us_filter.derivative(distance)}")
            us_filter.add(distance)
            distance = us_filter.values[len(us_filter.values) - 1]
            #print(f"Distance: {distance}")

            readColor = C_SENSOR.get_rgb()
            color = Color(r,g,b)
            print(f"Predicted Color: {color.predict()}")
            

            if isinstance(until_what, int) or isinstance(until_what, float):
                if distance is not None and distance < until_what:  # stop when close to wall
                    LEFT_MOTOR.set_dps(0)
                    RIGHT_MOTOR.set_dps(0)
                    print("ended current distance task")
                    break
            elif isinstance(until_what, str):
                if str(color).lower() == until_what.lower():
                    LEFT_MOTOR.set_dps(0)
                    RIGHT_MOTOR.set_dps(0)
                    print("ended current color task")
                    break
            else:
                raise Exception("unsupported type used. supported types: int (dist), float (dist), str (color)")

            time.sleep(SENSOR_POLL_SLEEP)

        except SensorError:
            print("An error occurred")
            stop_robot()
            break

    us_filter.clear()

if __name__ == '__main__':
    wait_ready_sensors()
    run(37.6)
