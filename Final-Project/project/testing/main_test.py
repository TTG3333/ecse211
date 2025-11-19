from utils import sound
from utils.color import Color
from utils.brick import Motor, EV3GyroSensor, EV3UltrasonicSensor, wait_ready_sensors, EV3ColorSensor
from time import sleep
import line_follower
import package_delivery
import gyro_turn

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
GYRO_SENSOR = EV3GyroSensor(4)
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")
C_SENSOR = EV3ColorSensor(1)

DISTANCE_TO_WALL = 12
distances_to_turn_at = [37.6, 37.6, 37.6, 86.1]  # Stack for all 4 rooms

#naive path function, goes to all rooms, should be made smarter later
successfulDeliveries = 0 

def restricted_room():
    restricted = False
    #  move slightly forward (check for red square)
    LEFT_MOTOR.set_dps(-line_follower.BACKUP_SPEED)
    RIGHT_MOTOR.set_dps(-line_follower.BACKUP_SPEED)
    sleep(0.5)
    line_follower.stop_robot()
    #  checks for red square
    r, g, b, lum = C_SENSOR.get_value()
    color = Color(r, g, b)
    if str(color).lower() == "red":
        restricted = True
    return restricted

def enter_next_room():
    line_follower.run(distances_to_turn_at.pop() - 5)
    gyro_turn.turn_90_deg('left')
    line_follower.run('orange')
    line_follower.stop_robot()  # stop at the orange door, then enter intra-room subsystem

def exit_current_room():
    gyro_turn.turn_180_deg()
    line_follower.run(DISTANCE_TO_WALL - 4)
    gyro_turn.turn_90_deg('left')

def deliver_to_next_room():
    '''Enters and exits the next room'''
    line_follower.run(distances_to_turn_at.pop() - 5)
    print(line_follower.us_filter.values)
    gyro_turn.turn_90_deg('left')
    line_follower.run('orange')
    gyro_turn.turn_180_deg()
    line_follower.run(DISTANCE_TO_WALL - 4)
    line_follower.us_filter.clear()
    gyro_turn.turn_90_deg('left')

if __name__ == "__main__":
    wait_ready_sensors() 
    sleep(1)
    # run until delivery 1
    deliver_to_next_room()

    # delivery 2
    deliver_to_next_room()
    line_follower.run(DISTANCE_TO_WALL - 4)

    #enter_next_room()
    #exit_current_room()
    #restricted = restricted_room()
    #if restricted:
    #    LEFT_MOTOR.set_dps(line_follower.BACKUP_SPEED)
    #    RIGHT_MOTOR.set_dps(line_follower.BACKUP_SPEED)
    #    sleep(0.5)
    #    line_follower.stop_robot()
    #    exit_current_room()
    #    enter_next_room()


