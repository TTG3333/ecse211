'''
Data obtained through testing:

    White:      H[] S[] V[]
    Black:      H[] S[] V[]

    Red:        H[] S[] V[]
    Orange:     H[] S[] V[]
    Yellow:     H[] S[] V[]
    Green:      H[] S[] V[]
    Blue:       H[] S[] V[]

'''

class Color:
    hues = {}       # The hues corresponding to certain colors.
    values = {}     # The values corresponding to certain shades.

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
        self.saturation = delta / cmax # (Assuming cmax is never 0 (very improbable))
        
        self.hue = 60 * (
            ((self.g - self.b) / delta) % 6             if cmax == self.r
                else ((self.b - self.r) / delta) + 2    if cmax == self.g
                else ((self.r - self.g) / delta) + 4    if cmax == self.b
                else 0
        )

    def __str__(self):
        '''
        Returns a string of the shade seen **OR** the color seen.

        If Saturation is found to be low, this means that it is a Shade
        Otherwise, we consider it a color.
        '''


