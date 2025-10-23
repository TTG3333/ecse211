import time
from utils.brick import Motor, wait_ready_sensors, TouchSensor

STATE = 0
DRUM_MOTOR = Motor("A")
DRUM_MOTOR.reset_encoder()

BPMS = [120, 180, 240, 300]  # Off, Slow, Medium, Fast

def next_state():
    """Increment the motor state to the next, or roll around if the end has been reached"""
    global STATE
    STATE = (STATE + 1) % (len(BPMS) + 1)

def set_drum_bpm(bpm: int):
    """Set the drum motor speed in BPM"""
    DRUM_MOTOR.set_dps(6 * bpm)

def stop_drum():
    """Stop the drum motor and reset state"""
    global STATE
    STATE = 0
    DRUM_MOTOR.set_dps(0)

def runner(speed_picker):
    """Main runner function to handle drum speed changes based on speed picker sensor"""
    if speed_picker.is_pressed():
        next_state() # Increment to next state
        print(f"Motor Speed: {STATE if STATE == 0 else BPMS[STATE - 1]} BPM")
        if STATE == 0:
            stop_drum()
        else:
            set_drum_bpm(BPMS[STATE - 1])
        time.sleep(0.5)  # Debounce delay

# -- Testing Section -- #
if __name__ == "__main__":
    SPEED_PICKER = TouchSensor(2)
    wait_ready_sensors()
    while True:
        runner(SPEED_PICKER)
        time.sleep(0.1)