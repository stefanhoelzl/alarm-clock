import uasyncio as asyncio

try:
    from mocks.peripherials import daylight
    from mocks.peripherials import indicator
    from mocks.peripherials import snooze_button
    from mocks.peripherials import switch
except ImportError:
    from .peripherials import daylight
    from .peripherials import indicator
    from .peripherials import snooze_button
    from .peripherials import switch


from apps.alarm_clock.alarm import Alarm


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
