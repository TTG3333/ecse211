"""
Main program to run the final project robot.
"""

from utils.brick    import Motor, EV3GyroSensor, EV3UltrasonicSensor, EV3ColorSensor, TouchSensor, wait_ready_sensors, BP

from utils.sounds   import play_clear, play_estop
from utils.room     import init_r, handle_room, stop_room
from utils.driver   import init_d, follow_line, stop_moving, drive_straight
from utils.turning  import init_t, turn_until_combined, stop_turning, turn_angle, turn_until

from time           import sleep
from os             import _exit

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

# Initial Configuration
SENSOR_POLL_SLEEP = 0.1

# E-Stop Configuration
ESTOP_POLL_SLEEP = 0.1

# Outline Configuration
ROOMS               = [[82, 33], [33], [33], []]
WALL_DISTANCE       = 8
END_ROOM_DISTANCE   = 57.5

# Speed Configuration
LINE_FOLLOWER_MULT      = 1.6
LINE_FOLLOWER_END_MULT  = 1.65
EMPTY_SPEED_MULT        = 2

# Angle Configurations
TURNING_OVERSHOOT_ROOM = 10

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
    delivery_status = handle_room()

    # Turn back to exit the room
    turn_angle(175, direction='right', until_colors=["Black"])
    drive_straight(until_distance=WALL_DISTANCE)
    
    return delivery_status

def handle_crash(args):
    # Stop all movement and sound
    stop_moving(); stop_turning(); stop_room()
    sa.stop_all()
    BP.reset_all()

    _exit(1) # Propagate error to close program

def main():
    # Initializes all subsystems
    init_d(*INITIALIZER)
    init_t(*INITIALIZER)
    init_r(*INITIALIZER)

    # Variables to determine if can end task early
    deliveries = 0
    current_pos = 0

    # Navigate through all the rooms 
    for line in ROOMS:
        for room_dist in line:
            # Check if no more deliveries
            if deliveries >= 2:
                break

            # Follow the line and enter the room
            print(f"Going to room at distance: {room_dist}")
            follow_line(until_distance=room_dist, speed_multiplier=LINE_FOLLOWER_MULT)

            delivery_status = room_procedure()

            # End position variable updates
            deliveries += 1 if delivery_status == "delivered" else 0
            current_pos += 1

            turn_until(direction='left', until_colors=["Black"], angle_after_color=TURNING_OVERSHOOT_ROOM)

        # No more rooms in the line, navigate to the end of the line and turn left.
        follow_line(speed_multiplier=LINE_FOLLOWER_END_MULT)
        turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
        if deliveries >= 2:
            print("Scanned all rooms. Ending scan.")
            break

    # Fastest path to the blue area
    if current_pos == 2: 
        # Case 1 - end after 2 rooms
        print("Navigating to end from Room 2")
        follow_line(speed_multiplier=EMPTY_SPEED_MULT) # Until the end of the line
        turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
        print("Landing on End Room Line")
        follow_line(until_distance=END_ROOM_DISTANCE, speed_multiplier=EMPTY_SPEED_MULT)

    # Fastest path to the blue area
    if current_pos == 3: 
        # Case 2 - end after 3 rooms
        print("Navigating to end from Room 3")
        print("Landing on End Room Line")
        follow_line(until_distance=END_ROOM_DISTANCE, speed_multiplier=EMPTY_SPEED_MULT)
        
    elif current_pos == 4:
        # Case 3 - end after 4 rooms
        print("Navigating to end from Room 4")
        follow_line(speed_multiplier=LINE_FOLLOWER_END_MULT)
        turn_until_combined(direction='left',   colors_list=[["Black"], ["White"]])
        print("Landing on End Room Line")
        follow_line(until_distance=END_ROOM_DISTANCE, speed_multiplier=EMPTY_SPEED_MULT)
        
    # Final stretch
    turn_until_combined(direction='left', colors_list=[["Black"], ["White"]])
    follow_line(until_colors=["Orange"], speed_multiplier=EMPTY_SPEED_MULT)
    drive_straight(until_colors=["Blue"], delay=1.5)

    # Play the clear sound and exit the program
    play_clear().wait_done()

if __name__ == "__main__":
    # Wait for all initialization of sensors.
    wait_ready_sensors()
    sleep(2)  # Small delay to ensure stability
    while US_SENSOR.get_value() == 0:
        sleep(SENSOR_POLL_SLEEP)

    # Starts listening to the Emergency Stop
    threading.excepthook = handle_crash
    t = threading.Thread(target=estop_handler, daemon=True)
    t.start()
    main()
