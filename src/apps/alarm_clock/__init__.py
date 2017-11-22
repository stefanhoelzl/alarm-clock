import utime as time
from uaos import App
from .alarm import Alarm
from .tasks import alarm_handler, off_switch, snoozer


class OffSwitch(App):
    async def __call__(self):
        await off_switch()
OffSwitch.register()


class Snoozer(App):
    async def __call__(self):
        await snoozer()
Snoozer.register()


class AlarmClock(App):
    requires = ['Apify', 'NTP']

    def __init__(self):
        super().__init__()
        l = time.localtime()
        h = l[Alarm.HOUR]
        m = l[Alarm.MINUTE] + 1
        a = Alarm.activated(h, m, daylight_time=30, snooze_time=10)
        print("Time to ring:", (a.time - time.time()))

    async def __call__(self):
        await alarm_handler()

AlarmClock.register()
