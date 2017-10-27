import ntp
import uasyncio as asyncio

from settings import TIME_ZONE

from alarm_clock.peripherials import daylight
from alarm_clock.peripherials import switch
from alarm_clock.peripherials import indicator
from alarm_clock.peripherials import snooze_button

from alarm_clock.alarm import Alarm

async def alarm_handler():
    while True:
        ringing = any((alarm.ringing for alarm in Alarm.all))
        if ringing:
            indicator.on()
        else:
            indicator.off()
        dl = max((alarm.daylight for alarm in Alarm.all))
        daylight.set(dl)
        await asyncio.sleep(1)

async def off_switch():
    while True:
        await switch
        for alarm in Alarm.all:
            if alarm.ringing:
                alarm.off()

async def snoozer():
    while True:
        await snooze_button
        for alarm in Alarm.all:
            if alarm.ringing:
                alarm.snooze()

async def time_update():
    while True:
        await asyncio.sleep(3600)
        ntp.settime(tz=TIME_ZONE)
