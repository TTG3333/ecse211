import time
from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, reset_brick, wait_ready_sensors

DELAY_SEC = 0.01
EMERGENCY_STOP = TouchSensor(1)
US_SENSOR = EV3UltrasonicSensor(3)

DISTANCES = [5, 7, 10, 13]
NOTES = ["C4", "E4", "G4", "C5"]

def mapping_distance(distance):
    """
    Change the values to the distance of the keys used.
    Keep into account any possible noise (actual distance +- 1/2cm)
    Discard any value above the distance of the furthest key
    """
    if distance is None:  # account for failed readings
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
    
def runner():
    distance = US_SENSOR.get_value()
    flute_note = mapping_distance(distance)
    print(f"Distance: {distance} cm - Flute Note: {flute_note}")

    if flute_note:
        SOUND = sound.Sound(duration=0.1, pitch=flute_note, volume=100)
        SOUND.play()
        SOUND.wait_done() # This yields, main may need to use multithreading.

if __name__ == "__main__":
    wait_ready_sensors()
    while True:
        runner()
        time.sleep(0.1)
