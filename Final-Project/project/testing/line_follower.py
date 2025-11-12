#  This current version works when the robot is initially placed on top of the black line, or slightly to the left.
#  If the robot was initially placed more to the right of the black line, it would drift away from the line.

from utils.brick import BP, Motor, wait_ready_sensors, SensorError, EV3UltrasonicSensor, EV3ColorSensor
import time
from math import pi
from package_delivery import move_to_next

#  we should test the color sensor beforehand to see what values we get
#  for white, and black and use those
WHITE_SURFACE = 175  # all 3 values should be close to 255
BLACK_LINE = 20      # all 3 values should be close to 0
THRESHOLD = (WHITE_SURFACE + BLACK_LINE) / 2 - 10
TOLERANCE = 20

#  adjust speed if needed
BASE_SPEED = -200
TURNING_SPEED = -220

SENSOR_POLL_SLEEP = 0.05

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
    print("STRAIGHT")
    LEFT_MOTOR.set_dps(BASE_SPEED)
    RIGHT_MOTOR.set_dps(BASE_SPEED)


def drive_slightly_left():
    print("LEFT")
    LEFT_MOTOR.set_dps(BASE_SPEED)
    RIGHT_MOTOR.set_dps(TURNING_SPEED)


def drive_slightly_right():
    print("RIGHT")
    LEFT_MOTOR.set_dps(TURNING_SPEED)
    RIGHT_MOTOR.set_dps(BASE_SPEED)


def follow_line(rgb_average):
    #  drift slightly left if closer to black line
    if rgb_average < THRESHOLD - TOLERANCE:
        drive_slightly_left()
    #  get back to the black line
    elif rgb_average > THRESHOLD + TOLERANCE:
        drive_slightly_right()
    else:
        drive_straight()


def stop_robot():
    LEFT_MOTOR.set_dps(0)
    RIGHT_MOTOR.set_dps(0)


def run():

    wait_ready_sensors()

    while True:
        try:
            r, g, b, lum = C_SENSOR.get_value()
            print(r, g, b)
            avg = average_rgb_value(r, g, b)
            print("Average:", str(avg))
            
            # stop on green square
            if b < 25 and abs(r-b) > :
                stop_robot()
                move_to_next()
                time.sleep(SENSOR_POLL_SLEEP)
                continue

            # follow line
            follow_line(avg)

            distance = US_SENSOR.get_value()
            if distance < 12:  # stop when close to wall
                LEFT_MOTOR.set_dps(0)
                RIGHT_MOTOR.set_dps(0)
                break

            time.sleep(SENSOR_POLL_SLEEP)

        except SensorError:
            stop_robot()
            break

    BP.reset_all()

if __name__=='__main__':
    run()
