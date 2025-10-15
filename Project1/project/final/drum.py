import time
from utils import sound
from utils.brick import Motor, TouchSensor, wait_ready_sensors

EMERGENCY_STOP = TouchSensor(1)
SPEED_PICKER = TouchSensor(2)

STATE = 0
DRUM_MOTOR = Motor("A")
DRUM_MOTOR.reset_encoder()

BPMS = [120, 180, 240, 300]  # Off, Slow, Medium, Fast

def next_state():
    global STATE
    STATE = (STATE + 1) % (BPMS.__len__() + 1)

def set_drum_bpm(bpm: int):
    DRUM_MOTOR.set_dps(6 * bpm)

def stop_drum():
    DRUM_MOTOR.set_dps(0)

def runner():
    if SPEED_PICKER.is_pressed():
        next_state() # Increment to next state
        print(f"STATE: {STATE}")
        if STATE == 0:
            stop_drum()
        else:
            set_drum_bpm(BPMS[STATE - 1])

# -- Testing Section -- #
if __name__ == "__main__":
    wait_ready_sensors()
    while True:
        runner()
        time.sleep(0.1)