#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=85)
TOUCH_SENSOR = TouchSensor(1)

SOUND_D4 = sound.Sound(duration=0.25, pitch="D4", volume=85)
SOUND_D5 = sound.Sound(duration=0.5, pitch="D5", volume=85)
SOUND_A4 = sound.Sound(duration=0.75, pitch="D4", volume=85)
SOUND_GS4 = sound.Sound(duration=0.5, pitch="G#4", volume=85)
SOUND_G4long = sound.Sound(duration=0.5, pitch="G4", volume=85)
SOUND_G4short = sound.Sound(duration=0.25, pitch="G4", volume=85)
SOUND_F4long = sound.Sound(duration=0.5, pitch="F4", volume=85)
SOUND_F4short = sound.Sound(duration=0.25, pitch="F4", volume=85)


wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()

def play_thefunny():
    "Play Megalovania"
    SOUND_D4.play()
    SOUND_D4.wait_done()
    SOUND_D4.play()
    SOUND_D4.wait_done()
    SOUND_D5.play()
    SOUND_D5.wait_done()
    SOUND_A4.play()
    SOUND_A4.wait_done()
    SOUND_GS4.play()
    SOUND_GS4.wait_done()
    SOUND_G4long.play()
    SOUND_G4long.wait_done()
    SOUND_F4long.play()
    SOUND_F4long.wait_done()
    SOUND_D4.play()
    SOUND_D4.wait_done()
    SOUND_F4short.play()
    SOUND_F4short.wait_done()
    SOUND_G4short.play()
    SOUND_G4short.wait_done()


def play_sound_on_button_press():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            pressed = TOUCH_SENSOR.is_pressed()
            if (pressed == True):
                play_thefunny()
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        exit()


if __name__=='__main__':
    play_sound()

    # TODO Implement this function
    play_sound_on_button_press()
