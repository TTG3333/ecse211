class Color:
    def __init__(self, r, g, b):
        # Default values for the color
        self.r = r / 255
        self.g = g / 255
        self.b = b / 255

        # Additional HSV values for the color
        cmax = max(self.r,self.g,self.b)
        cmin = min(self.r,self.g,self.b)
        delta = (cmax - cmin)
        
        self.value = cmax
        self.saturation = delta / cmax # (Assuming cmax is never 0)
        
        self.hue = 60 * (
            ((self.g - self.b) / delta) % 6             if cmax == self.r
                else ((self.b - self.r) / delta) + 2    if cmax == self.g
                else ((self.r - self.g) / delta) + 4    if cmax == self.b
                else 0
        )

    # def __str__(self):
        