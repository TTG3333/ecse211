from utils.brick import Motor

DRUM_MOTOR = Motor("D")
DRUM_MOTOR.set_limits(power=50, dps=360*6) # (Max 100 BPM)

def drum_at_bpm(bpm: int):
    # Rotates the drum motor at a certain BPM.
    DRUM_MOTOR.set_dps(360 * bpm / 60)

def stop_drum():
    DRUM_MOTOR.set_dps(0)