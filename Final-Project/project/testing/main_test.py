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

#naive path function, goes to all rooms, should be made smarter later
successfulDeliveries = 0

def delivery():
    gyro_turn.turn_90_deg('left')
    line_follower.run('orange') #no check for red yet
    #package_delivery()
    gyro_turn.turn_180_deg()
    line_follower.run(6.5)
    gyro_turn.turn_90_deg('left')

if __name__ == "__main__":
    wait_ready_sensors() 
    # run until delivery 1
    line_follower.run(81)
    delivery()

    # delivery 2
    line_follower.run(32.5)
    delivery()

    package_delivery.move_to_next()
