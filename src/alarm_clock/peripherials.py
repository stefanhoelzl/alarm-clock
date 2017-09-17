import uasyncio as asyncio

import machine
import neopixel

import hw


def deinit():
    daylight.deinit()
    indicator.deinit()

class Daylight(object):
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


class Indicator(object):
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


class Switch(object):
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
