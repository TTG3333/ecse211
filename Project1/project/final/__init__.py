from .drum import *
from .note_detection import *

def main():
    wait_ready_sensors()
    while True:
        drum.runner()
        note_detection.runner()
        time.sleep(0.1)

if __name__ == "__main__":
    main()