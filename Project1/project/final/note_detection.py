from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep

DELAY_SEC = 0.01
TOUCH_SENSOR = TouchSensor(1)  # enter correct port
US_SENSOR = EV3UltrasonicSensor(2)  # enter correct port

wait_ready_sensors(True)

def mapping_distance(distance):
    """
    Change the values to the distance of the keys used.
    Keep into account any possible noise (actual distance +- 1/2cm)
    Discard any value above the distance of the furthest key
    """
    if distance is None:  # account for failed readings
        return None
    elif distance <= 7:
        return "A4"
    elif distance <= 12:
        return "B4"
    elif distance <= 17:
        return "C4"
    elif distance <= 22:
        return "D4"
    else:
        return None  # discard odd values (e.g. 255)

def note_detection():
    # start on first button press
    while not TOUCH_SENSOR.is_pressed():
        pass
    sleep(0.5)
    note_being_played = False  # wait for key to be lowered before playing another sound

    try:
        while not TOUCH_SENSOR.is_pressed():  # halt at emergency stop
            distance = US_SENSOR.get_value()
            flute_note = mapping_distance(distance)

            if flute_note and not note_being_played:
                SOUND = sound.Sound(duration=0.3, pitch=flute_note, volume=85)
                SOUND.play()
                SOUND.wait_done()
                note_being_played = True

            elif flute_note is None:
                note_being_played = False

            sleep(DELAY_SEC)
    except BaseException:
        pass
    finally:
        reset_brick()
        exit()

if __name__ == "__main__":
    note_detection()
