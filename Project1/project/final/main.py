from . import drum
from . import note_detection

import time
import threading

from utils.brick import wait_ready_sensors

def main():
    wait_ready_sensors()

    # Note handling part:
    threading.Thread(target=note_detection.runner, daemon=True).start()
    def drum_handler():
        while True:
            drum.runner()
            time.sleep(0.25)

    def note_handler():
        while True:
            note_detection.runner()
            time.sleep(0.1)

    t1 = threading.Thread(target=drum_handler, daemon=True).start()
    t2 = threading.Thread(target=note_handler, daemon=True).start()

if __name__ == "__main__":
    main()