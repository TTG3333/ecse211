import math
import csv

# Configurable parameters

CONFIDENCE_EXPONENT = 2

# ##################### #

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

    def predict(self):
        '''
        Returns a string of the predicted color, and certainty factor.
        '''

        distances = {}
        self_vector = self.hue_vect()

        # Hard coded results
        if self.value < 0.25:
            return ("Black", 1)
        elif self.saturation < 0.2:
            return ("White", 1)

        for ref, label in Color.colors:
            viewed_vector = ref.hue_vect()

            dist = math.sqrt(
                (viewed_vector[0] - self_vector[0]) ** 2 + 
                (viewed_vector[1] - self_vector[1]) ** 2 +
                (self.value - ref.value) ** 2
            )

            if label not in distances or dist < distances[label]:
                distances[label] = dist

        sorted_labels = sorted(distances.items(), key=lambda x: x[1])
        (label1, dist1), (label2, dist2) = sorted_labels[:2]

        certainty = 1 - (dist1 / dist2) ** CONFIDENCE_EXPONENT

        return (label1, certainty)
    
    def lerp(self, color, alpha):
        return Color(
            (color.r - self.r) * alpha + self.r,
            (color.g - self.g) * alpha + self.g,
            (color.b - self.b) * alpha + self.b,
        )

    def __str__(self):
        '''
        Returns the string of the predict function
        '''
        name, _ = self.predict()
        return name

    def hue_vect(self):
        h0 = math.cos(math.radians(self.hue))
        h1 = math.sin(math.radians(self.hue))
        return (h0, h1)

# Add additional data values:
Color.colors = []

with open("../collection/color_data.csv", "r") as colors:
    reader = csv.reader(colors)
    next(reader) # Ignore header

    for r,g,b,label in reader:
        Color.colors.append([
            Color(int(r),int(g),int(b)),
            label
        ])
