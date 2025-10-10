from utils.brick import Motor

DRUM_MOTOR = Motor("D")
DRUM_MOTOR.set_limits(power=50, dps=360*6) # (Max 100 BPM)

def drum_at_bpm(bpm: int):
    # Rotates the drum motor at a certain BPM.
    DRUM_MOTOR.set_dps(360 * bpm / 60)

def stop_drum():
    DRUM_MOTOR.set_dps(0)


if __name__ == "__main__":
    # Test area for drum motor
    import time

    drum_at_bpm(60)
    time.sleep(10)
    stop_drum()
    time.sleep(2)
    drum_at_bpm(120)