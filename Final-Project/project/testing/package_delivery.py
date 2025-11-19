from utils.brick import BP, Motor, wait_ready_sensors
import time
from math import pi

# All in cm
BELT_DIAMETER = 3.5
CUBE_SIZE = 2.5
CUBE_SPACING = 0.8

BELT_MOTOR = Motor("B")
BELT_MOTOR.reset_encoder()

def move_to_next():
    # Calculate the distance to move
    distance = CUBE_SIZE + CUBE_SPACING
    # Calculate the circumference of the belt
    circumference = BELT_DIAMETER * pi
    # Calculate the number of rotations needed
    rotations = distance / circumference
    # Convert rotations to degrees
    degrees = rotations * 360

    # Move the belt motor
    BELT_MOTOR.set_limits(dps=90)
    BELT_MOTOR.set_position_relative(-degrees)
    time.sleep(degrees/90 + 0.5)  # Wait for the movement to complete, the wait_is_stopped doesn't seem to work reliably

def run():
    wait_ready_sensors()

    try:
        for _ in range(3):  # Move 5 cubes as a test
            move_to_next()
            print("Finished")
            time.sleep(5)  # Pause between moves
    finally:
        BP.reset_all()

if __name__ == "__main__":
    run()