from utils.brick import Motor

DRUM_MOTOR = Motor("D")
DRUM_MOTOR.reset_encoder()
DRUM_MOTOR.set_limits(power=50, dps=360*10) # (Max 100 BPM)
DRUM_MOTOR.set_power(50) # Discovered that 100 Power crashes the pi...

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
    print("Stopping drum")
    stop_drum()
    time.sleep(2)
    print("Starting drum at 100 BPM")
    drum_at_bpm(100)
    stop_drum()