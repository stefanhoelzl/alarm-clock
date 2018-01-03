import ujson as json
import os

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

    storage = "/storage/alarm_clock.json"

    def __init__(self):
        super().__init__()
        self.auto_store = True
        self.alarms = {}
        self.load()
        self.loop = asyncio.get_event_loop()
        self.running_tasks = []
        peripherials.switch.callback = self.off

    def as_list(self, state=True):
        ret = []
        for aid, alarm in self.alarms.items():
            a = alarm.as_dict(state=state)
            a["aid"] = aid
            ret.append(a)
        return ret

    def from_list(self, lst):
        for a in lst:
            self.create(**a)

    def create(self, hour, minute, days=None,
               daylight_mode=None, daylight_time=None,
               snooze_time=None, enabled=True, aid=None, **kwargs):
        al = Alarm(hour, minute, days=days,
                   daylight_time=daylight_time, daylight_mode=daylight_mode,
                   snooze_time=snooze_time, enabled=enabled)
        if not aid:
            for aid in range(len(self.alarms)):
                if aid not in self.alarms:
                    break
            else:
                aid = len(self.alarms)
        else:
            aid = int(aid)
        self.alarms[aid] = al

        if self.auto_store:
            self.store()

    def store(self):
        lst = self.as_list(state=False)
        js = json.dumps(lst)
        with open(self.storage, "w") as f:
            f.write(js)

    def load(self):
        auto_store = self.auto_store
        self.auto_store = False

        if "alarm_clock.json" in os.listdir("/storage"):
            with open(self.storage, "r") as f:
                js = f.read()
            lst = json.loads(js)
            if not isinstance(lst, list):
                lst = []
            self.from_list(lst)

        self.auto_store = auto_store

    def delete(self, aid):
        del self.alarms[aid]
        if self.auto_store: self.store()

    def enable(self, aid):
        self.alarms[aid].enable()
        if self.auto_store: self.store()

    def disable(self, aid):
        self.alarms[aid].disable()
        if self.auto_store: self.store()

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
            # if self.ringing:
            if self.daylight:
                self.loop.create_task(self.wait_for_snooze())
                peripherials.indicator.on()
            else:
                peripherials.indicator.off()
            peripherials.daylight.set(self.daylight)
            await asyncio.sleep(1)

    @singelton_task("SNOOZE")
    async def wait_for_snooze(self):
        while (not peripherials.snooze_button.triggered) and self.daylight:
            await asyncio.sleep(0.1)
        #if self.ringing:
        if self.daylight:
            self.off()
            # self.snooze()

AlarmClockApp.register()
