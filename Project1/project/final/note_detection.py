import time
import threading

from utils import sound
from utils.brick import wait_ready_sensors, EV3UltrasonicSensor

DIST_ERR = 0.2
DELAY_SEC = 0.01

MIN_DISTANCE = 3 # Ignore anything below this distance (cm)
DISTANCES = [5, 7, 10, 13]
NOTES = ["C4", "E4", "G4", "C5"]
NOTE_SOUNDS = {note:sound.Sound(duration=5, pitch=note, volume=80) for note in NOTES}
for s in NOTE_SOUNDS.values():
    s.repeat_sound(24, 0)  # Repeat for a long time

CURRENT_NOTE = None
CURRENT_SOUND = None

class NoiseEliminator:
    """ Helper class to filter out noise in sensor readings
    Keeps a rolling list of the last `total_vals` readings,
    uses a circular buffer to store them."""
    def __init__(self, total_vals, min_vals):
        self.total_vals = total_vals
        self.min_vals = min_vals
        self.values = [None] * total_vals
        self.index = 0
    
    def add_value(self, value):
        self.values[self.index] = value
        self.index = (self.index + 1) % self.total_vals
    
    def get_filtered_value(self):
        """ Returns the most repeated value in the buffer, ignoring None values.
        If not enough valid values, returns None."""
        valid_values = [v for v in self.values if v is not None]
        if not valid_values or len(valid_values) < self.min_vals:
            return None
        
        organized = {}
        for v in valid_values:
            k = round(v / DIST_ERR) * DIST_ERR
            if k in organized:
                organized[k] += 1
            else:
                organized[k] = 1
        highest = max(organized.keys(), key=lambda k: organized[k])
        return highest
    
    def get_median_value(self):
        """ Returns the median value in the buffer, ignoring None values.
        If not enough valid values, returns None."""
        valid_values = [v for v in self.values if v is not None]
        if not valid_values or len(valid_values) < self.min_vals:
            return None
        sorted_values = sorted(valid_values)
        mid = len(sorted_values) // 2
        if len(sorted_values) % 2 == 0:
            return sorted_values[mid]
            # (sorted_values[mid - 1] + sorted_values[mid]) / 2 
            # This code caused issues, because it would often play higher notes due to averaging
        else:
            return sorted_values[mid]


NOISE_HANDLER = NoiseEliminator(20, 16)

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
            CURRENT_SOUND = NOTE_SOUNDS[note]
            CURRENT_SOUND.play()
        CURRENT_NOTE = note

def stop_note():
    global CURRENT_NOTE, CURRENT_SOUND
    if CURRENT_SOUND is not None:
        CURRENT_SOUND.stop()
        CURRENT_SOUND = None
    CURRENT_NOTE = None
    
def runner(us_sensor, stopped=False):
    distance = us_sensor.get_value()
    NOISE_HANDLER.add_value(distance)
    if not stopped:
        distance = NOISE_HANDLER.get_most_repeated()
        #distance = NOISE_HANDLER.get_median_value()
        flute_note = mapping_distance(distance)
        # NOISE_HANDLER.add_value(flute_note)
        # flute_note = NOISE_HANDLER.get_filtered_value()
        # print(f"Distance: {distance} cm - Flute Note: {flute_note}")
        play_note(flute_note)

if __name__ == "__main__":
    US_SENSOR = EV3UltrasonicSensor(3)
    wait_ready_sensors()
    while True:
        runner(US_SENSOR)
        time.sleep(0.1)
