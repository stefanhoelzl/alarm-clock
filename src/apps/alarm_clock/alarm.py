from .alarm_states import *
from apps.ntp import NTP

class Alarm(StateMachine):
    INITIAL_STATE = Enabled

    def __init__(self, h=0, m=0, days=None,
                 daylight_mode=None, daylight_time=None,
                 snooze_time=0, enabled=True):
        self.hour = h
        self.minute = m
        self.time = None
        self.days = days
        self.daylight_mode = daylight_mode
        self.daylight_time = daylight_time
        self.snooze_time = snooze_time
        self.snooze_counter = 0
        init_state = Enabled if enabled else Disabled
        StateMachine.__init__(self, initial_state=init_state(self))

    def as_dict(self, state=False):
        dct = {
            "hour": self.hour,
            "minute": self.minute,
            "days": self.days,
            "daylight_mode": self.daylight_mode,
            "daylight_time": self.daylight_time,
            "snooze_time": self.snooze_time,
            "enabled": self == Enabled
        }
        if state:
            dct.update({
                "daylight": self.daylight,
                "ringing": self.ringing,
                "snoozing": self.snoozing,
                "time_left": self.time_left
            })
        return dct

    @property
    def daylight(self):
        if self == Daylight:
            daylight_time = self.daylight_time
            if self.daylight_mode:
                daylight = (daylight_time - self.time_left) / daylight_time
                return max(0.0, min(1.0, daylight))
        return 0

    @property
    def ringing(self):
        return self == Ringing

    @property
    def snoozing(self):
        return self == Snoozing

    @property
    def time_left(self):
        if self == Enabled:
            return self.time - NTP.time()
        return None

    def snooze(self):
        self.transition(Snooze())

    def off(self):
        self.transition(Off())

    def enable(self):
        self.transition(Enable())

    def disable(self):
        self.transition(Disable())

    def update(self):
        self.transition(Update(NTP.time()))
