'''
    Another main test file
'''

from utils.brick    import Motor, EV3GyroSensor, EV3UltrasonicSensor, EV3ColorSensor, wait_ready_sensors

from utils.driver   import init_d, follow_line
from utils.turning  import init_t, turn_until_combined

# ---------------------------------------------------- #
# Configurable settings

# Sensors Configuration
GYRO_SENSOR         = EV3GyroSensor(4)
COLOR_SENSOR        = EV3ColorSensor(1)
US_SENSOR           = EV3UltrasonicSensor(3)

# Motor Configuration
LEFT_MOTOR          = Motor("A")
RIGHT_MOTOR         = Motor("D")

# Initialization Configuration
INITIALIZER         = (COLOR_SENSOR, GYRO_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR)

# Outline Configuration
ROOMS               = [[82, 33], [33], [33], []]
WALL_DISTANCE       = 8
# ---------------------------------------------------- #

def room_procedure():
    turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
    follow_line(until_colors=["Orange"])
    # [ Scan room here ]
    turn_until_combined(direction='right',  colors_list=[["Black"], ["White"]])
    follow_line(until_distance=WALL_DISTANCE)
    turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])

if __name__ == "__main__":  
    wait_ready_sensors()
    init_d(*INITIALIZER)
    init_t(*INITIALIZER)

    for line in ROOMS:
        for room_dist in line:
            # Follow the line and enter the room
            follow_line(until_distance=room_dist)
            room_procedure()

        # No more rooms, navigate to the end of the line and turn left.
        follow_line()
        turn_until_combined(direction='left', colors_list=[["Black"], ["White"]])

    follow_line()
    turn_until_combined(direction='left', colors_list=[["Black"], ["White"]])

