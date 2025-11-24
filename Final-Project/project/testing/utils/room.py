#!/usr/bin/env python3

'''
    Main helper used for the intra-room subsystem.
    Provides useful functions for scanning in a room.

    Before using, please use wait_ready_sensors in another file.
'''

from utils.color    import Color

# ---------------------------------------------------- #
# Configurable settings

## Turning Configurations
ANGLE_TURN = 1

## Certainty Behavior
COLOR_CERTAINTY = True

# ---------------------------------------------------- #