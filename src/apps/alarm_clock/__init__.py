import uasyncio as asyncio

from uaos import App
from .alarm import Alarm

try:
    from mocks import peripherials
except ImportError:
    from . import peripherials

from apps.alarm_clock.alarm import Alarm


def singelton_task(name):
    def decorator(task):
        async def wrapper(self):
            if name not in self.running_tasks:
                self.running_tasks.append(name)
                await task(self)
                self.running_tasks.remove(name)
        return wrapper
    return decorator


class AlarmClock(App):
    requires = ['Apify', 'NTP']

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.running_tasks = []

    @property
    def ringing(self):
        return any((a.ringing for a in Alarm.all))

    @property
    def daylight(self):
        return max((a.daylight for a in Alarm.all))

    @property
    def snoozing(self):
        return any((a.snoozing for a in Alarm.all))

    def snooze(self):
        for a in Alarm.all:
            if a.ringing:
                a.snooze()
        peripherials.indicator.off()

    def off(self):
        for a in Alarm.all:
            if a.ringing or a.snoozing:
                a.off()
        peripherials.indicator.off()
        peripherials.switch.callback = None

    def on(self):
        peripherials.switch.callback = self.off
        self.loop.create_task(self.wait_for_snooze())
        peripherials.indicator.on()

    async def __call__(self):
        while True:
            if self.ringing:
                self.on()
            peripherials.daylight.set(self.daylight)
            await asyncio.sleep(1)

    @singelton_task("SNOOZE")
    async def wait_for_snooze(self):
        while (not peripherials.snooze_button.triggered) and self.ringing:
            await asyncio.sleep(0.1)
        if self.ringing:
            self.snooze()

AlarmClock.register()