import math
import csv

class Color:
    def __init__(self, r, g, b):
        '''
        Constructs a color object, which allows to read the R,G,B H,S,V values.
        '''

        # Default values for the color
        self.r = r / 255
        self.g = g / 255
        self.b = b / 255

        # Additional HSV values for the color
        cmax = max(self.r,self.g,self.b)
        cmin = min(self.r,self.g,self.b)
        delta = (cmax - cmin)
        
        self.value = cmax
        self.saturation = delta / cmax if cmax != 0 else 0
        
        self.hue = 60 * (
            0                                           if delta == 0
                else ((self.g - self.b) / delta) % 6    if cmax == self.r
                else ((self.b - self.r) / delta) + 2    if cmax == self.g
                else ((self.r - self.g) / delta) + 4
        )

    def __str__(self):
        '''
        Returns a string of the shade seen **OR** the color seen.

        If Saturation is found to be low, this means that it is a Shade
        Otherwise, we consider it a color.
        '''

        n, ldist = None, None

        # Edge cases (white/black)
        if self.value < 0.15:
            return "Black"
        elif self.value > 0.55:
            return "White"

        vect = self.hue_vect()

        for ref, label in Color.colors:
            vect2 = ref.hue_vect()
            dist = math.sqrt(
                    (vect2[0] - vect[0]) ** 2 + 
                    (vect2[1] - vect[1]) ** 2 +
                    (self.value - ref.value) ** 2
                )

            if ldist is None or dist < ldist:
                n = label; ldist = dist 

        return n

    def hue_vect(self):
        h0 = math.cos(math.radians(self.hue))
        h1 = math.sin(math.radians(self.hue))
        return (h0, h1)
    
Color.colors = []

# Add additional data values:
with open("../collection/color_data.csv", "r") as colors:
    reader = csv.reader(colors)
    next(reader) # Ignore header

    for r,g,b,label in reader:
        Color.colors.append([
            Color(int(r),int(g),int(b)),
            label
        ])