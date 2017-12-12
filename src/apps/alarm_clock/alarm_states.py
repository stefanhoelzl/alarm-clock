import time

from .state_machine import State, event, StateMachine
from .alarm_time import next_time
from .alarm_events import *


class AlarmState(State):
    def __init__(self, sm):
        self.alarm = sm
        super().__init__(sm)


class Disabled(AlarmState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alarm.time = None

    @event(Enable)
    def enable(self, e):
        return Enabled


class Enabled(AlarmState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(self) == Enabled:
            self.alarm.time = next_time(self.alarm.hour, self.alarm.minute,
                                        days=self.alarm.days,
                                        current_time=self.alarm.time)
            self.alarm.snooze_counter = 0

    @event(Update)
    def update(self, e):
        if self.alarm.daylight_mode \
                and e.time >= (self.alarm.time - self.alarm.daylight_time):
            return Daylight
        elif e.time >= self.alarm.time:
            return Ringing

    @event(Disable)
    def disable(self, e):
        return Disabled


class Daylight(Enabled):
    disable = Enabled.disable

    @event(Off)
    def off(self, e):
        if self.alarm.days:
            return Enabled
        return Disabled

    @event(Update)
    def update(self, e):
        if e.time >= self.alarm.time:
            return Ringing


class Ringing(Daylight):
    off = Daylight.off
    disable = Enabled.disable


    @event(Snooze)
    def snooze(self, e):
        if self.alarm.snooze_time:
            return Snoozing


class Snoozing(Daylight):
    def __init__(self, alarm, *args, **kwargs):
        super().__init__(alarm, *args, **kwargs)
        self.alarm.snooze_counter += 1
        self.alarm.snooze_until = self.alarm.time + self.alarm.snooze_counter*self.alarm.snooze_time

    off = Daylight.off
    disable = Enabled.disable

    @event(Update)
    def update(self, e):
        if e.time >= self.alarm.snooze_until:
            return Ringing

