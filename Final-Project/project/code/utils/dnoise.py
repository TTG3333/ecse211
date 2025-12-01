#!/usr/bin/env python3

'''
    Derivative based cache.
'''

from time       import monotonic

# ---------------------------------------------------- #

class dNoise:
    def __init__(self, max_slope):
        self.max_slope = max_slope
        self.last = None
        self.time = monotonic()

    def add(self, val):
        current = monotonic()

        if self.last is not None:
            dt = current - self.time
            if dt > 0:
                if abs(val - self.last) / dt > self.max_slope:
                    return False

        self.last = val
        self.time = current
        return True

    def derivative(self, value):
        if self.last is None:
            return 0

        dt = monotonic() - self.time
        if dt == 0:
            return 0

        return abs(value - self.last) / dt

    def clear(self):
        self.last = None
        self.time = monotonic()

    def get(self):
        return self.last

    def __call__(self):
        return self.get()