import math
import uasyncio as asyncio

import machine
import neopixel

import hw

from .hal import HCSR04


def deinit():
    daylight.deinit()
    indicator.deinit()


class Daylight:
    DEFAULT_KELVIN = 2500

    @staticmethod
    def kelvin_to_rgb(kelvin):
        temp = kelvin / 100
        if temp <= 66:
            red = 255
            green = 99.4708025861 * math.log(temp) - 161.1195681661
            if temp <= 19:
                blue = 0
            else:
                blue = 138.5177312231 * math.log(temp-10) - 305.0447927307
        else:
            red = 329.698727446 * math.pow(temp - 60, -0.1332047592)
            green = 288.1221695283 * math.pow(temp - 60, -0.0755148492)
            blue = 255
        return (
            min(255, max(0, red)),
            min(255, max(0, green)),
            min(255, max(0, blue))
        )

    def __init__(self):
        self.np = neopixel.NeoPixel(machine.Pin(hw.LED_SPI), hw.LED_COUNT,
                                    timing=True)
        self.last = None
        self.set(0)

    def set(self, i, kelvin=DEFAULT_KELVIN):
        if self.last is None or (i, kelvin) != self.last:
            self.last = (i, kelvin)
            rgb = tuple(map(lambda x: int(x*i),
                            Daylight.kelvin_to_rgb(kelvin)))
            self.np.fill(rgb)
            self.np.write()

    def deinit(self):
        self.set(0)
daylight = Daylight()


class Indicator:
    def __init__(self):
        self.pin = machine.Pin(hw.LED0, machine.Pin.OUT)
        self.off()

    def on(self):
        self.pin.value(True)

    def off(self):
        self.pin.value(False)

    def deinit(self):
        self.off()
indicator = Indicator()


class Switch:
    def __init__(self):
        self.callback = None
        self.pin = machine.Pin(hw.BUTTON, machine.Pin.IN)
        self.pin.irq(handler=self.press, trigger=machine.Pin.IRQ_FALLING)

    def press(self, p):
        if self.callback:
            self.callback()

switch = Switch()


class SnoozeButton:
    TRIGGER_DISTANCE_MM = 40

    def __init__(self):
        self.hcsr04 = HCSR04(hw.HCSR04_ECHO, hw.HCSR04_TRIGGER, max_m=0.1)

    @property
    def triggered(self):
        mm = (self.hcsr04.mm, self.hcsr04.mm)
        if all(mm) and 0.5*sum(mm) < self.TRIGGER_DISTANCE_MM:
            return True
        return False

snooze_button = SnoozeButton()
