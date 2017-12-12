from .alarm import Alarm
from .api import *

try:
    from mocks import peripherials
except ImportError:
    from . import peripherials


def singelton_task(name):
    def decorator(task):
        async def wrapper(self):
            if name not in self.running_tasks:
                self.running_tasks.append(name)
                await task(self)
                self.running_tasks.remove(name)
        return wrapper
    return decorator


class AlarmClockApp(App):
    requires = ['Apify', 'NTP']

    def __init__(self):
        super().__init__()
        self.alarms = {}
        self.loop = asyncio.get_event_loop()
        self.running_tasks = []
        peripherials.switch.callback = self.off

    def create(self, hour, minute, days=None,
               dl_mode=None, dl_time=None,
               snooze=None):
        al = Alarm(hour, minute, days=days,
                   daylight_time=dl_time, daylight_mode=dl_mode,
                   snooze_time=snooze)
        for aid in range(len(self.alarms)):
            if aid not in self.alarms:
                break
        else:
            aid = len(self.alarms)
        self.alarms[aid] = al

    def delete(self, aid):
        del self.alarms[aid]

    @property
    def ringing(self):
        return any((a.ringing for a in self.alarms.values()))

    @property
    def daylight(self):
        if self.alarms:
            return max((a.daylight for a in self.alarms.values()))
        return 0

    @property
    def snoozing(self):
        return any((a.snoozing for a in self.alarms.values()))

    def snooze(self):
        for a in self.alarms.values():
            a.snooze()

    def off(self):
        for a in self.alarms.values():
            a.off()

    async def __call__(self):
        while True:
            for a in self.alarms.values():
                a.update()
            if self.ringing:
                self.loop.create_task(self.wait_for_snooze())
                peripherials.indicator.on()
            else:
                peripherials.indicator.off()
            peripherials.daylight.set(self.daylight)
            await asyncio.sleep(1)

    @singelton_task("SNOOZE")
    async def wait_for_snooze(self):
        while (not peripherials.snooze_button.triggered) and self.ringing:
            await asyncio.sleep(0.1)
        if self.ringing:
            self.snooze()

AlarmClockApp.register()