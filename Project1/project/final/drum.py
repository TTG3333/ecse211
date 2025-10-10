from utils.brick import Motor

DRUM_MOTOR = Motor("D")
DRUM_MOTOR.set_limits(power=100, dps=360*10) # (Max 100 BPM)
DRUM_MOTOR.set_power(100)
DRUM_MOTOR.reset_encoder()

def drum_at_bpm(bpm: int):
    # Rotates the drum motor at a certain BPM.
    DRUM_MOTOR.set_dps((-1) * 360 * bpm / 60)

def stop_drum():
    DRUM_MOTOR.set_dps(0)


if __name__ == "__main__":
    # Test area for drum motor
    import time

    drum_at_bpm(30)
    time.sleep(10)
    stop_drum()
    time.sleep(2)
    drum_at_bpm(100)