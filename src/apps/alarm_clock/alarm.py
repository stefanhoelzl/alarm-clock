from .alarm_states import *


class Alarm(StateMachine):
    def __init__(self, h=0, m=0, days=None, daylight_time=None, snooze_time=0):
        super().__init__()
        self.hour = h
        self.minute = m
        self.time = None
        self.days = days
        self.daylight_time = daylight_time
        self.snooze_time = snooze_time
        self.enable()

    @property
    def daylight(self):
        if self == Daylight:
            return self.state.daylight
        return 0

    @property
    def ringing(self):
        return self == Ringing

    @property
    def snoozing(self):
        return self == Snoozing

    @property
    def time_left(self):
        return self.time - time.time()

    def snooze(self):
        self.transition(Snooze)

    def off(self):
        self.transition(Off)

    def enable(self):
        self.transition(Enable)

    def disable(self):
        self.transition(Disable)

    def update(self):
        self.transition(Update)
