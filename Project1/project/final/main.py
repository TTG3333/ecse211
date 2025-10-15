import drum
import note_detection

import time
import threading

from utils.brick import wait_ready_sensors, TouchSensor, EV3UltrasonicSensor

ESTOP_PRESSED = False

EMERGENCY_STOP = TouchSensor(1)
SPEED_PICKER = TouchSensor(2)
US_SENSOR = EV3UltrasonicSensor(3)

def main():
    print("Initializing sensors...")
    wait_ready_sensors()
    print("Sensors ready. Starting main loop.")

    # Note handling part:
    def drum_handler():
        while True:
            if ESTOP_PRESSED:
                drum.stop_drum()
            else:
                drum.runner(SPEED_PICKER)
            time.sleep(0.15)

    def note_handler():
        while True:
            if not ESTOP_PRESSED:
                note_detection.runner(US_SENSOR)
            else:
                time.sleep(0.1)

    def estop_handler():
        while True:
            if EMERGENCY_STOP.is_pressed():
                ESTOP_PRESSED = not ESTOP_PRESSED
                time.sleep(0.5)  # Debounce delay
            time.sleep(0.1)

    t1 = threading.Thread(target=drum_handler)
    t2 = threading.Thread(target=note_handler)
    t3 = threading.Thread(target=estop_handler)
    t1.start()
    t2.start()
    t3.start()

if __name__ == "__main__":
    main()