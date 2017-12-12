class NeoPixel:
    def __init__(self, pin, count, timing=True):
        self.pin = pin
        self.count = count
        self.r = 0
        self.g = 0
        self.b = 0

    def fill(self, rgb):
        self.r, self.g, self.b = rgb

    def write(self):
        pass
