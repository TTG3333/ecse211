from utils import sound
from utils.color import Color
from utils.brick import Motor, EV3GyroSensor, EV3UltrasonicSensor, wait_ready_sensors
from time import sleep
import line_follower
import package_delivery
import gyro_turn

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
GYRO_SENSOR = EV3GyroSensor(4)
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

DISTANCE_TO_WALL = 12
distances_to_turn_at = [37.6, 37.6, 37.6, 86.1]  # Stack for all 4 rooms

#naive path function, goes to all rooms, should be made smarter later
successfulDeliveries = 0 

def check_for_restricted_room():
    '''Checks for red square'''
    print("")

def deliver_to_next_room():
    '''Enters and exits the next room'''
    line_follower.run(distances_to_turn_at.pop() - 5)
    gyro_turn.turn_90_deg('left')
    line_follower.run('orange')
    gyro_turn.turn_180_deg()
    line_follower.run(DISTANCE_TO_WALL - 4)
    gyro_turn.turn_90_deg('left')

if __name__ == "__main__":
    wait_ready_sensors() 
    # run until delivery 1
    deliver_to_next_room()

    # delivery 2
    deliver_to_next_room()
    line_follower.run(DISTANCE_TO_WALL - 4)
