import time
from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, reset_brick, wait_ready_sensors

DELAY_SEC = 0.01
EMERGENCY_STOP = TouchSensor(1)
US_SENSOR = EV3UltrasonicSensor(3)

NOTES = ["A4", "B4", "C4", "D4"]

def mapping_distance(distance):
    """
    Change the values to the distance of the keys used.
    Keep into account any possible noise (actual distance +- 1/2cm)
    Discard any value above the distance of the furthest key
    """
    if distance is None:  # account for failed readings
        return None
    elif distance <= 5:
        return NOTES[0]
    elif distance <= 7:
        return NOTES[1]
    elif distance <= 10:
        return NOTES[2]
    elif distance <= 13:
        return NOTES[3]
    else:
        return None  # discard odd values (e.g. 255)
    
def runner():
    distance = US_SENSOR.get_value()
    print(f"Distance: {distance} cm")
    flute_note = mapping_distance(distance)
    print(f"Flute Note: {flute_note}")

    if flute_note:
        SOUND = sound.Sound(duration=0.1, pitch=flute_note, volume=100)
        SOUND.play()
        SOUND.wait_done()

if __name__ == "__main__":
    wait_ready_sensors()
    while True:
        runner()
        time.sleep(0.1)
