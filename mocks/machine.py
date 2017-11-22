class Pin:
    OUT = 0
    IN = 1

    IRQ_FALLING = 0

    def __init__(self, pin, mode=OUT, pull=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull

    def on(self):
        pass

    def off(self):
        pass

    def irq(self, handler, trigger):
        pass

    def value(self, val):
        pass

class RTC:
    @staticmethod
    def datetime(tm):
        pass

def time_pulse_us(pin, mode, us):
    pass
