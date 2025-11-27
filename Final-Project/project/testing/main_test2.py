'''
    Another main test file
'''

from utils.brick    import Motor, EV3GyroSensor, EV3UltrasonicSensor, EV3ColorSensor, TouchSensor, wait_ready_sensors

from utils.sounds   import play_clear, play_estop
from utils.room     import init_r, handle_room, stop_room
from utils.driver   import init_d, follow_line, stop_moving, drive_straight
from utils.turning  import init_t, turn_until_combined, stop_turning, turn_angle

from time           import sleep

import threading
import simpleaudio  as sa

# ---------------------------------------------------- #
# Configurable settings

# Sensors Configuration
COLOR_SENSOR        = EV3ColorSensor(1)
TOUCH_SENSOR        = TouchSensor(2)
US_SENSOR           = EV3UltrasonicSensor(3)
GYRO_SENSOR         = EV3GyroSensor(4)

# Motor Configuration
LEFT_MOTOR          = Motor("A")
PACKAGE_MOTOR       = Motor("B")
RIGHT_MOTOR         = Motor("D")

# E-Stop Configuration
ESTOP_POLL_SLEEP = 0.1

# Outline Configuration
ROOMS               = [[82, 33], [33], [33], []]
WALL_DISTANCE       = 8
END_ROOM_DISTANCE   = 57.5

# Initialization Configuration
INITIALIZER         = (COLOR_SENSOR, GYRO_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR, PACKAGE_MOTOR)
# ---------------------------------------------------- #

def estop_handler():
    while True:
        if TOUCH_SENSOR.is_pressed():
            break
        sleep(ESTOP_POLL_SLEEP)

    raise Exception

def room_procedure():
    # Navigate to the orange
    turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
    follow_line(until_colors=["Orange"])
    
    # Scan the room and deliver package if applicable
    delivered = handle_room()

    # Turn back to exit the room
    turn_angle(180, direction='right')
    drive_straight(until_distance=WALL_DISTANCE)
    
    # Get back on the original path
    turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
    return delivered

def handle_crash(args):
    # Stop all movement
    stop_moving(); stop_turning(); stop_room()

    # Play Emergency Sound
    sa.stop_all()
    # play_estop().wait_done() # Play an emergency sound

    raise args.exc_value # Propagate error to close program

if __name__ == "__main__":
    # Wait for all initialization of sensors.
    wait_ready_sensors()

    # Starts listening to the Emergency Stop
    threading.excepthook = handle_crash
    t = threading.Thread(target=estop_handler, daemon=True)
    t.start()

    # Initializes all subsystems
    init_d(*INITIALIZER)
    init_t(*INITIALIZER)
    init_r(*INITIALIZER)

    # Navigate through all the rooms 
    for line in ROOMS:
        for room_dist in line:
            # Follow the line and enter the room
            follow_line(until_distance=room_dist)
            print(f"Package delivered: {room_procedure()}")

        # No more rooms in the line, navigate to the end of the line and turn left.
        follow_line()
        turn_until_combined(direction='left', colors_list=[["Black"], ["White"]])

    # Navigate to the blue area
    follow_line(until_distance=END_ROOM_DISTANCE)
    turn_until_combined(direction='left', colors_list=[["Black"], ["White"]])
    follow_line(until_colors=["Orange"])
    drive_straight(until_colors=["Blue"], delay=0.5)

    # Play the clear sound and exit the program
    play_clear().wait_done()