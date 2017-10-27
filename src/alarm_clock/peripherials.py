import uasyncio as asyncio

import machine
import neopixel

import hw

from .hal import HCSR04


def deinit():
    daylight.deinit()
    indicator.deinit()


class Daylight:
    def __init__(self):
        self.np = neopixel.NeoPixel(machine.Pin(hw.LED_SPI), hw.LED_COUNT)
        self.set(0)

    def set(self, i):
        i = int(255*i)
        self.np.fill((i, i, i))
        self.np.write()

    def deinit(self):
        self.set(0)
daylight = Daylight()


class Indicator:
    def __init__(self):
        self.pin = machine.Pin(hw.LED0, machine.Pin.OUT)
        self.off()

    def on(self):
        self.pin.off()

    def off(self):
        self.pin.on()

    def deinit(self):
        self.off()
indicator = Indicator()


class Switch:
    def __init__(self):
        self.pressed = False
        self.pin = machine.Pin(hw.BUTTON, machine.Pin.IN)
        self.pin.irq(handler=self.press, trigger=machine.Pin.IRQ_FALLING)

    def press(self, p):
        self.pressed = True

    def __await__(self):
        while not self.pressed:
            yield from asyncio.sleep(0)
        self.pressed = False

    __iter__ = __await__
switch = Switch()


class SnoozeButton:
    TRIGGER_DISTANCE_MM = 40

    def __init__(self):
        self.hcsr04 = HCSR04(hw.HCSR04_ECHO, hw.HCSR04_TRIGGER)

    @property
    def triggered(self):
        mm = self.hcsr04.mm
        if mm and mm > self.TRIGGER_DISTANCE_MM:
            return True
        return False

    def __await__(self):
        while not self.hcsr04.mm > self.TRIGGER_DISTANCE_MM:
            yield from asyncio.sleep(0.1)

    __iter__ = __await__
snooze_button = SnoozeButton()
