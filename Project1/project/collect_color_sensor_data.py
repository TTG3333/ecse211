#!/usr/bin/env python3
# In this part, you will implement a discrete color sampler using the touch sensor.
# In the collect_color_sensor_data.py file, complete the collect_color_sensor_data() function
# such that when the touch sensor is pressed once, the program reads and prints the RGB values
# from the color sensor once, then writes the values to a file. The number of measurements should
# be equal to the number of touch sensor presses.

# The code should contain:
# -	A statement to open the output file (refer to collect_us_sensor_data.py for an example).
# -	A while loop that continuously samples the color sensor.
# -	An if statement that checks for the touch sensor status.
# -	An action to write the color sensor reading to the output file when conditions are met.


"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import BP, EV3ColorSensor, wait_ready_sensors, TouchSensor, SensorError
from time import sleep


COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

SENSOR_POLL_SLEEP = 0.05

# complete this based on your hardware setup
C_SENSOR = EV3ColorSensor(3)
T_SENSOR = TouchSensor(1)

wait_ready_sensors(True)  # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    """Collect color sensor data."""
    try:
        while not T_SENSOR.is_pressed():  # wait for the user to press the touch sensor to start
            sleep(SENSOR_POLL_SLEEP)
        sleep(1)  # debounce delay so that the script doesn't immediately stop
        f = open(COLOR_SENSOR_DATA_FILE, "w+")
        num_samples = 0  # keep track of number of sample points
        while True:
            try:
                if T_SENSOR.is_pressed():  # check to see if the button is pressed again to stop
                    break
                num_samples += 1
                red, gre, blu, lum = C_SENSOR.get_value()
                f.write(f"{red},{gre},{blu}\n")
                print(f"{red},{gre},{blu}")
                sleep(SENSOR_POLL_SLEEP)  # wait before polling the sensor again
            except SensorError as error:
                print(error)
                exit()
    except KeyboardInterrupt:  # stop sampling with (Ctrl-C)
        pass
    finally:
        print("Done collecting color samples")
        print(f"Collected {num_samples} samples")
        f.close()
        BP.reset_all()  # Turn off everything on the brick's hardware, and reset it


if __name__ == "__main__":
    collect_color_sensor_data()
