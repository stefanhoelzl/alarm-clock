try:
    import utime as time
except ImportError:
    import time


def seconds(hours, minutes):
    return (hours*60 + minutes)*60


class Alarm:
    def __init__(self):
        self.enabled = True
        self.daylight_time = None
        self.snooze_time = 0
        self.hour = 0
        self.minute = 0

        self.time = 0
        self.snooze_counter = 0

    @property
    def daylight(self):
        if not self.daylight_time or not self.enabled:
            return 0.0
        daylight = (self.daylight_time - self.time_left)/self.daylight_time
        return max(0.0, min(1.0, daylight))

    @property
    def ringing(self):
        return self.time_left <= 0 and not self.snoozing and self.enabled

    @property
    def time_left(self):
        return self.time - time.time()

    @property
    def snoozing(self):
        if self.time_left > 0:
            return False
        return self.snooze_counter*self.snooze_time > -self.time_left

    def set_time(self):
        current_time = time.time()
        t = list(time.localtime(current_time))
        t[3] = self.hour
        t[4] = self.minute
        alarm_time = time.mktime(tuple(t))
        if alarm_time <= current_time:
            alarm_time += seconds(24, 0)
        self.time = alarm_time

    def snooze(self):
        self.snooze_counter += 1

    def off(self):
        self.enabled = False

    def activate(self):
        self.set_time()
        self.snooze_counter = 0
        self.enabled = True

    def deactivate(self):
        self.enabled = False
