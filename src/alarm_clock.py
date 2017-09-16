import machine
import neopixel
import ntp
import uasyncio as asyncio
import hw
import utime as time


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


class AlarmIndicator(object):
    def __init__(self):
        self.pin = machine.Pin(hw.LED0, machine.Pin.OUT)
        self.off()

    def on(self):
        self.pin.off()

    def off(self):
        self.pin.on()

    def deinit(self):
        self.off()
alarm_indicator = AlarmIndicator()


class AlarmSwitch(object):
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
alarm_switch = AlarmSwitch()

async def set_alarm(at, f):
    asyncio.get_event_loop().create_task(alarm(time.mktime(at), f))

async def time_update():
    while True:
        ntp.settime(tz=2)
        await asyncio.sleep(3600)

async def alarm(alarm_time, daylight_forerun):
    dt = alarm_time - time.time() - daylight_forerun
    await asyncio.sleep(dt)
    while alarm_time > time.time():
        dt = alarm_time - time.time()
        daylight.set(1 - (float(dt)/daylight_forerun))
        await asyncio.sleep(1)
    daylight.set(1)
    alarm_indicator.on()
    await alarm_switch
    alarm_indicator.off()
    daylight.set(0)

async def timeout(t):
    await asyncio.sleep(t)

loop = asyncio.get_event_loop()
loop.create_task(time_update())
loop.create_task(set_alarm((2017, 9, 16, 17, 53, 0, 0, 0), 10))
loop.run_forever()
loop.close()

daylight.deinit()
alarm_indicator.deinit()
