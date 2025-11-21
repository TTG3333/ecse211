'''
    Another main test file
'''

from time           import sleep

from utils.brick    import (Motor, EV3GyroSensor, EV3UltrasonicSensor, EV3ColorSensor, wait_ready_sensors)

from utils.driver   import init_d, follow_line
from utils.turning  import init_t, turn_until

# ---------------------------------------------------- #
GYRO_SENSOR         = EV3GyroSensor(4)
COLOR_SENSOR        = EV3ColorSensor(1)
US_SENSOR           = EV3UltrasonicSensor(3)

LEFT_MOTOR          = Motor("A")
RIGHT_MOTOR         = Motor("D")

INITIALIZER         = (COLOR_SENSOR, GYRO_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR)
# ---------------------------------------------------- #

if __name__ == "__main__":  
    wait_ready_sensors()
    init_d(*INITIALIZER)
    init_t(*INITIALIZER)

    follow_line(84.5 + 5)
    turn_until('left', colors=["Black"])