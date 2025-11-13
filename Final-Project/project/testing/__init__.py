from utils.brick import wait_ready_sensors, TouchSensor, EV3UltrasonicSensor
from . import line_follower, gyro_turn

line_follower.run()
gyro_turn.turn_90_deg('left')
line_follower.run()

