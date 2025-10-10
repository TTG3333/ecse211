from utils.brick import Motor

DRUM_MOTOR = Motor("D")
DRUM_MOTOR.reset_encoder()

def drum_at_bpm_rot(bpm: int):
    # Rotates the drum motor at a certain BPM.
    DRUM_MOTOR.set_dps(360 * bpm / 60)

def stop_drum():
    DRUM_MOTOR.set_dps(0)

# drum_bpm
# drum_stop

if __name__ == "__main__":
    # Test area for drum motor
    import time

    drum_at_bpm_rot(60)
    time.sleep(2)
    stop_drum()
    time.sleep(2)
    drum_at_bpm_rot(1000)
    time.sleep(2)
    stop_drum()
