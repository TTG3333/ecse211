print("Importing modules...")


import time
import threading
import simpleaudio as sa

from utils.brick import wait_ready_sensors, TouchSensor, EV3UltrasonicSensor, EV3GyroSensor, EV3ColorSensor
print("Modules imported.")

recorder = sa.WaveObject.from_wave_file("../sounds/help.wav")
PLAYER = None
ESTOP_PLAYER = None

ESTOP_PRESSED = False

COLOUR_SENSOR = EV3ColorSensor(1)
EMERGENCY_STOP = TouchSensor(2)
US_SENSOR = EV3UltrasonicSensor(3)
GYRO_SENSOR = EV3GyroSensor(4)

def main():
    """Main function for the robot"""
    print("Initializing sensors...")
    wait_ready_sensors()
    print("Sensors ready. Starting main loop.")

    # Note handling part:
    def main_thread():
        """Main thread for robot operation"""
        global ESTOP_PRESSED, PLAYER, ESTOP_PLAYER
        while True:
            if ESTOP_PRESSED:
                if not ESTOP_PLAYER or not ESTOP_PLAYER.is_playing():
                    if not PLAYER or not PLAYER.is_playing():
                        PLAYER = recorder.play()
            else:
                if PLAYER:
                    PLAYER.stop()
                    PLAYER = None
                    sa.WaveObject.from_wave_file("../sounds/collect.wav").play().wait_done()
                    time.sleep(0.1)
                    sa.WaveObject.from_wave_file("../sounds/clear.wav").play().wait_done()
            time.sleep(0.1)

    def estop_handler():
        """Emergency stop handler to toggle ESTOP_PRESSED state"""
        global ESTOP_PRESSED, ESTOP_PLAYER
        while True:
            if EMERGENCY_STOP.is_pressed():
                ESTOP_PRESSED = not ESTOP_PRESSED
                print(f"Emergency Stop {'Activated' if ESTOP_PRESSED else 'Deactivated'}")
                if ESTOP_PRESSED:
                    ESTOP_PLAYER = sa.WaveObject.from_wave_file("../sounds/estop.wav").play()
                time.sleep(0.5)  # Debounce delay
            time.sleep(0.1)

    t1 = threading.Thread(target=main_thread)
    t2 = threading.Thread(target=estop_handler)
    t1.start()
    t2.start()

if __name__ == "__main__":
    main()