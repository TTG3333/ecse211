'''
    Another main test file
'''

from utils.brick    import Motor, EV3GyroSensor, EV3UltrasonicSensor, EV3ColorSensor, TouchSensor, wait_ready_sensors

from utils.driver   import init_d, follow_line
from utils.turning  import init_t, turn_until_combined
from utils.room     import init_r, handle_room
from utils.sounds   import play_clear, play_estop

from time           import sleep
from threading      import Thread

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

# Initialization Configuration
INITIALIZER         = (COLOR_SENSOR, GYRO_SENSOR, US_SENSOR, LEFT_MOTOR, RIGHT_MOTOR, PACKAGE_MOTOR)

# E-Stop Configuration
ESTOP_POLL_SLEEP = 0.1
FINISHED = False

# Outline Configuration
ROOMS               = [[82, 33], [33], [33], []]
WALL_DISTANCE       = 8
# ---------------------------------------------------- #

def estop_handler():
    global FINISHED
    while True:
        if FINISHED:
            break
        if TOUCH_SENSOR.is_pressed():
            s = play_estop()
            # Stop all subsystems
            s.wait_done()
            raise Exception
        sleep(ESTOP_POLL_SLEEP)

def room_procedure():
    turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
    follow_line(until_colors=["Orange"])
    delivered = handle_room()
    turn_until_combined(direction='right',  colors_list=[["Black"], ["White"]])
    follow_line(until_distance=WALL_DISTANCE)
    turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
    return delivered

if __name__ == "__main__":  
    wait_ready_sensors()
    t = Thread(target=estop_handler)
    t.start()
    init_d(*INITIALIZER)
    init_t(*INITIALIZER)
    init_r(*INITIALIZER)

    for line in ROOMS:
        for room_dist in line:
            # Follow the line and enter the room
            follow_line(until_distance=room_dist)
            print(f"Package delivered: {room_procedure()}")

        # No more rooms, navigate to the end of the line and turn left.
        follow_line()
        turn_until_combined(direction='left', colors_list=[["Black"], ["White"]])
    FINISHED = True
