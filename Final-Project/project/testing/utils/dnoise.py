import time

class dNoise:
    def __init__(self, max_slope, max):
        self.time = time.clock_gettime()
        self.max = max
        self.max_slope = max_slope
        self.values = []

    def add(self, val):
        current = time.clock_gettime()
        dt = current - self.time
        self.time = current

        if not self.values:
            self.values.append(val)
            return
        
        latest = self.values[len(self.values) - 1]
        if abs(val - latest) / dt < self.max_slope:
            self.values.append(val)
        
        if len(self.values) > (self.max - 1):
            self.values.pop(0)

    def median(self):
        vals = sorted(self.values)
        return vals[len(vals) // 2]