import time

class dNoise:
    def __init__(self, max_slope, max):
        self.time = 0
        self.max = max
        self.max_slope = max_slope
        self.values = []

    def add(self, val):
        '''
        Adds a value to the buffer only if the derivative between that 
            value and the last one is acceptable
        '''
        current = time.monotonic()
        dt = current - self.time
        self.time = current

        if not self.values:
            self.values.append(val)
            return
        
        latest = self.values[len(self.values) - 1]
        if abs(val - latest) / dt > self.max_slope:
            return False
        
        self.values.append(val)
        if len(self.values) > self.max:
            self.values.pop(0)

        return True
    
    def derivative(self, value):
        dt = time.monotonic() - self.time
        latest = self.values[len(self.values) - 1]
        return abs(value - latest) / dt

    def median(self):
        vals = sorted(self.values)
        return vals[len(vals) // 2]