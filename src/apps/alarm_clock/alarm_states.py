import time

from .state_machine import State, event, StateMachine
from .alarm_time import next_time
from .alarm_events import *


class AlarmState(State):
    def __init__(self, alarm, *args, **kwargs):
        super().__init__()
        self.alarm = alarm

    def to(self, state):
        return state(self.alarm)


class Disabled(AlarmState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alarm.time = None

    @event(Enable)
    def enable(self, e):
        return self.to(Enabled)


class Enabled(AlarmState):
    def __new__(cls, *args, **kwargs):
        return Inactive(*args, **kwargs)

    @event(Disable)
    def disable(self, e):
        return self.to(Disabled)


class Inactive(Enabled):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alarm.time = next_time(self.alarm.hour, self.alarm.minute,
                                    days=self.alarm.days)

    @event(Update)
    def update(self, e):
        if time.time() > (self.alarm.time - self.alarm.daylight_time):
            return self.to(Daylight)


class Daylight(Enabled):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def daylight(self):
        daylight_time = self.alarm.daylight_time
        daylight = (daylight_time - self.alarm.time_left) / daylight_time
        return max(0.0, min(1.0, daylight))

    @event(Update)
    def update(self, e):
        if time.time() > self.alarm.time:
            return self.to(Ringing)


class Ringing(Daylight):
    @event(Off)
    def off(self, e):
        if self.alarm.days:
            return self.to(Enabled)
        return self.to(Disabled)

    @event(Snooze)
    def snooze(self, e):
        return self.to(Snooze)


class Snoozing(Ringing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snooze_until = time.time() + self.alarm.snooze_time

    @event(Update)
    def update(self, e):
        if time.time() > self.snooze_until:
            return self.to(Ringing)

