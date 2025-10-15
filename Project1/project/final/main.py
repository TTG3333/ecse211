from . import drum
from . import note_detection
import time

from utils.brick import wait_ready_sensors

def main():
    wait_ready_sensors()
    while True:
        drum.runner()
        note_detection.runner()
        #time.sleep(0.1)

if __name__ == "__main__":
    main()