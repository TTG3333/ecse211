'''
Data obtained through testing:

    White:      S[0, 0.23]  V[0.6, 1]
    Black:      S[0, 0.35]  V[0, 0.15]

    Red:        H[] S[0.875] V[]
    Orange:     H[] S[] V[]
    Yellow:     H[] S[] V[]
    Green:      H[] S[] V[]
    Blue:       H[] S[] V[]

'''

class Color:
    hues    = {}        # The hues corresponding to certain colors.
    values  = {}        # The values corresponding to certain shades.

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
            0                                           if cmax == 0
                else ((self.g - self.b) / delta) % 6             if cmax == self.r
                else ((self.b - self.r) / delta) + 2    if cmax == self.g
                else ((self.r - self.g) / delta) + 4
        )

    def __str__(self):
        '''
        Returns a string of the shade seen **OR** the color seen.

        If Saturation is found to be low, this means that it is a Shade
        Otherwise, we consider it a color.
        '''


