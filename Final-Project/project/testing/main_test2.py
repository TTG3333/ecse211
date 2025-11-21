'''
    Another main test file
'''

from time           import sleep

from utils.brick    import (Motor, EV3GyroSensor, EV3UltrasonicSensor, EV3ColorSensor, wait_ready_sensors)

from utils.driver   import init_d, follow_line
from utils.turning  import init_t, turn_until, turn_90_deg, turn_180_deg

# ---------------------------------------------------- #
GYRO_SENSOR         = EV3GyroSensor(4)
COLOR_SENSOR        = EV3ColorSensor(1)
US_SENSOR           = EV3UltrasonicSensor(3)

LEFT_MOTOR          = Motor("A")
RIGHT_MOTOR         = Motor("D")

INITIALIZER         = (COLOR_SENSOR, GYRO_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR)
# ---------------------------------------------------- #

def room_procedure():
    turn_90_deg('left')
    follow_line(until_colors=["Orange"])
    ## Scan room
    turn_180_deg('right')
    follow_line(until_distance=13)
    turn_90_deg('left')

if __name__ == "__main__":  
    wait_ready_sensors()
    init_d(*INITIALIZER)
    init_t(*INITIALIZER)

    # --------------------------- #
    # Enter Room 1
    follow_line(until_distance=81)
    room_procedure()
    # --------------------------- #
