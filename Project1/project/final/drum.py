import time
from utils import sound
from utils.brick import Motor, TouchSensor, wait_ready_sensors

SOUND_1 = sound.Sound(duration=0.1, pitch="A4", volume=85)
SOUND_2 = sound.Sound(duration=0.1, pitch="C4", volume=85)

EMERGENCY_STOP = TouchSensor(1)
SPEED_PICKER = TouchSensor(2)

STATE = 0
DRUM_MOTOR = Motor("A")
DRUM_MOTOR.reset_encoder()

BPMS = [30, 60, 120]  # Off, Slow, Medium, Fast

def next_state():
    STATE = (STATE + 1) % 4

def set_drum_bpm(bpm: int):
    DRUM_MOTOR.set_dps(6 * bpm)

def stop_drum():
    DRUM_MOTOR.set_dps(0)

def runner():
    if SPEED_PICKER.is_pressed():
        next_state() # Increment to next state
        match STATE:
            case 0: # (Off)
                stop_drum()
            case 1: # (Slow)
                set_drum_bpm(BPMS[0])
            case 2: # (Medium)
                set_drum_bpm(BPMS[1])
            case 3: # (Fast)
                set_drum_bpm(BPMS[2])
            case _:
                pass

# -- Testing Section -- #
if __name__ == "__main__":
    wait_ready_sensors()
    while True:
        runner()
        time.sleep(0.1)