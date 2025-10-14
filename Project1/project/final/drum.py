from utils.brick import Motor, TouchSensor, wait_ready_sensors
from utils import sound
import time

SOUND_1 = sound.Sound(duration=0.1, pitch="A4", volume=85)
SOUND_2 = sound.Sound(duration=0.1, pitch="C4", volume=85)

EMERGENCY_STOP = TouchSensor(1)
SPEED_PICKER = TouchSensor(2)

DRUM_MOTOR = Motor("D")
DRUM_MOTOR.reset_encoder()

wait_ready_sensors()

def set_drum_bpm(bpm: int):
    DRUM_MOTOR.set_dps(6 * bpm)

def stop_drum():
    DRUM_MOTOR.set_dps(0)

if __name__ == "__main__":
    stop_drum()
    curr_speed = "off"

    while True:
        if EMERGENCY_STOP.is_pressed():
            raise Exception("Manual Emergency Exit!")

        elif SPEED_PICKER.is_pressed():
            while SPEED_PICKER.is_pressed():  # prevents continuous holding of button
                time.sleep(0.1)

            match curr_speed:
                case "off":
                    curr_speed = "slow"
                    SOUND_1.play()
                    time.sleep(0.5)
                    SOUND_2.play()
                    set_drum_bpm(30)
                case "slow":
                    curr_speed = "medium"
                    SOUND_1.play()
                    time.sleep(0.3)
                    SOUND_2.play()
                    set_drum_bpm(60)
                case "medium":
                    curr_speed = "fast"
                    SOUND_1.play()
                    time.sleep(0.1)
                    SOUND_2.play()
                    set_drum_bpm(120)
                case "fast":
                    curr_speed = "off"
                    SOUND_2.play()
                    time.sleep(0.5)
                    SOUND_1.play()
                    stop_drum()
                case _:
                    pass
