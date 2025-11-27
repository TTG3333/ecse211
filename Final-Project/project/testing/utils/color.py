#!/usr/bin/env python3

'''
    Main helper for color reading.

    Before using, please use wait_ready_sensors in another file.
'''

from math       import sin, cos, sqrt, radians
from csv        import reader

# ---------------------------------------------------- #

class Color:
    # Configurable Parameters
    ## Confidence Parameters
    CONFIDENCE_EXPONENT = 4         # How much the uncertainty grows
    CONFIDENCE_THRESHOLD = 0.75     # How much confidence the color needs

    ## Area Parameters
    VALUE_THRESHOLD_BLACK = 0.25        # Under this value, all colors      = black
    SATURATION_THRESHOLD_WHITE = 0.25   # Under this saturation, all colors = white

    ## Dataset Parameters
    DATASET_DIR = "../collection/color_data.csv"
    # ##################### #

    def __init__(self, r, g, b):
        '''
        Constructs a color object, which allows to read the R,G,B H,S,V values.
        '''

        # Default values for the color
        div = max(r,g,b,255)
        self.r = r / div
        self.g = g / div
        self.b = b / div

        # Additional HSV values for the color
        M = max(self.r,self.g,self.b)
        m = min(self.r,self.g,self.b)
        delta = (M - m)
        
        # Cache system
        self._prediction = None

        self.value = M
        self.saturation = delta / M if M != 0 else 0
        
        self.hue = 60 * (
            0                                           if delta == 0
                else ((self.g - self.b) / delta) % 6    if M == self.r
                else ((self.b - self.r) / delta) + 2    if M == self.g
                else ((self.r - self.g) / delta) + 4
        )

    def predict(self):
        '''
        Returns a string of the predicted color, and certainty factor.
        '''

        if self._prediction is None:
            distances = {}
            self_vector = self.hue_vect()

            # Hard coded results
            if self.value < self.VALUE_THRESHOLD_BLACK:
                self._prediction = ("Black", 1)
            elif self.saturation < self.SATURATION_THRESHOLD_WHITE:
                self._prediction = ("White", 1)
            else:
                for ref, label in Color.colors:
                    viewed_vector = ref.hue_vect()

                    dist = sqrt(
                        (viewed_vector[0] - self_vector[0]) ** 2 + # HueX
                        (viewed_vector[1] - self_vector[1]) ** 2 + # HueY
                        (self.value - ref.value) ** 2              # Value
                    )

                    if label not in distances or dist < distances[label]:
                        distances[label] = dist

                sorted_labels = sorted(distances.items(), key=lambda x: x[1])
                (label1, dist1), (_, dist2) = sorted_labels[:2]

                certainty = 1 - (dist1 / dist2) ** self.CONFIDENCE_EXPONENT
                self._prediction = (label1, certainty)

        return self._prediction
    
    def is_certain(self):
        '''
        Returns a bool to know if a reading is certain or not.
        '''
        (_, certainty) = self.predict()
        return certainty > self.CONFIDENCE_THRESHOLD
    
    def lerp(self, color, alpha):
        return Color(
            ((color.r - self.r) * alpha + self.r) * 255,
            ((color.g - self.g) * alpha + self.g) * 255,
            ((color.b - self.b) * alpha + self.b) * 255,
        )

    def hue_vect(self):
        '''
        Constructs the hue vector
        '''
        h0 = cos(radians(self.hue))
        h1 = sin(radians(self.hue))
        return (h0, h1)
    
    def __str__(self):
        '''
        Returns the string of the predict function
        '''
        name, _ = self.predict()
        return name

# Add additional data values:
Color.colors = []

with open(Color.DATASET_DIR) as colors:
    rd = reader(colors)
    next(rd) # Ignore header

    for r,g,b,label in rd:
        Color.colors.append([
            Color(int(r),int(g),int(b)),
            label
        ])
