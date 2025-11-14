from utils import sound, color
from utils.brick import Motor, EV3GyroSensor, EV3UltrasonicSensor, wait_ready_sensors
from time import sleep
import line_follower
import package_delivery

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
GYRO_SENSOR = EV3GyroSensor(4)
LEFT_MOTOR = Motor("A")
RIGHT_MOTOR = Motor("D")

wait_ready_sensors() 
