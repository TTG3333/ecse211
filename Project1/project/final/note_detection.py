import time
import threading

from utils import sound
from utils.brick import wait_ready_sensors, EV3UltrasonicSensor

DELAY_SEC = 0.01

MIN_DISTANCE = 3 # Ignore anything below this distance (cm)
DISTANCES = [5, 7, 10, 13]
NOTES = ["C4", "E4", "G4", "C5"]
CURRENT_NOTE = None
CURRENT_SOUND = None

def mapping_distance(distance):
    """
    Change the values to the distance of the keys used.
    Keep into account any possible noise (actual distance +- 1/2cm)
    Discard any value above the distance of the furthest key
    """
    if distance is None:  # account for failed readings
        return None
    elif distance < MIN_DISTANCE:
        return None
    elif distance <= DISTANCES[0]:
        return NOTES[0]
    elif distance <= DISTANCES[1]:
        return NOTES[1]
    elif distance <= DISTANCES[2]:
        return NOTES[2]
    elif distance <= DISTANCES[3]:
        return NOTES[3]
    else:
        return None  # discard odd values (e.g. 255)
    
def play_note(note):
    global CURRENT_NOTE, CURRENT_SOUND
    if note != CURRENT_NOTE:
        print(f"Playing note: {note}")
        if CURRENT_SOUND is not None:
            CURRENT_SOUND.stop()
            CURRENT_SOUND = None
        if note is not None:
            CURRENT_SOUND = sound.Sound(duration=0.2, pitch=note, volume=100)
            CURRENT_SOUND.repeat_sound(600, 0)  # Repeat for a long time
            CURRENT_SOUND.play()
        CURRENT_NOTE = note
    
def runner(us_sensor):
    distance = us_sensor.get_value()
    flute_note = mapping_distance(distance)
    # print(f"Distance: {distance} cm - Flute Note: {flute_note}")
    play_note(flute_note)

if __name__ == "__main__":
    US_SENSOR = EV3UltrasonicSensor(3)
    wait_ready_sensors()
    while True:
        runner(US_SENSOR)
        time.sleep(0.1)
