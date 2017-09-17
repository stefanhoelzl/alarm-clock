import ntp
import uasyncio as asyncio
import utime as time

from settings import TIME_ZONE

from alarm_clock.peripherials import daylight
from alarm_clock.peripherials import switch
from alarm_clock.peripherials import indicator

async def alarm(alarm_time, daylight_forerun):
    dt = alarm_time - time.time() - daylight_forerun
    await asyncio.sleep(dt)
    while alarm_time > time.time():
        dt = alarm_time - time.time()
        daylight.set(1 - (float(dt)/daylight_forerun))
        await asyncio.sleep(1)
    daylight.set(1)
    indicator.on()
    await switch
    indicator.off()
    daylight.set(0)

async def time_update():
    while True:
        ntp.settime(tz=TIME_ZONE)
        await asyncio.sleep(3600)
