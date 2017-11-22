import time


def seconds(hours, minutes):
    return (hours*60 + minutes)*60


class Alarm:
    YEAR = 0
    MONTH = 1
    DAY = 2
    HOUR = 3
    MINUTE = 4
    SECOND = 5
    WEEKDAY = 6
    YEARDAY = 7

    all = []

    @classmethod
    def activated(cls, h, m, days=None, daylight_time=None, snooze_time=None):
        alarm = Alarm()
        alarm.hour = h
        alarm.minute = m
        alarm.days = days
        alarm.daylight_time = daylight_time
        alarm.snooze_time = snooze_time
        alarm.activate()
        return alarm

    def __init__(self):
        self.enabled = False
        self.daylight_time = None
        self.snooze_time = 0
        self.hour = 0
        self.minute = 0
        self.days = None

        self.time = 0
        self.snooze_counter = 0

        Alarm.all.append(self)

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
        t[self.HOUR] = self.hour
        t[self.MINUTE] = self.minute
        t[self.SECOND] = 0
        alarm_time = time.mktime(tuple(t))
        if alarm_time <= current_time:
            alarm_time += seconds(24, 0)
        self.time = alarm_time

    @staticmethod
    def diff_between_weekdays(day0, day1):
        diff = day1 - day0
        if diff < 0:
            diff = (day1 + 7) - day0
        return diff

    def get_next_weekday(self, current_day):
        for day in sorted(self.days):
            if day > current_day:
                return day
        return min(self.days)

    def next_time(self):
        if not self.days:
            return None

        if self.time > time.time():
            return self.time

        t = list(time.localtime(self.time))
        current_day = t[self.WEEKDAY]
        next_day = self.get_next_weekday(current_day)

        diff = self.diff_between_weekdays(current_day, next_day)
        return 24*diff*60*60+self.time

    def snooze(self):
        self.snooze_counter += 1

    def off(self):
        if self.days:
            self.snooze_counter = 0
            self.time = self.next_time()
        else:
            self.deactivate()

    def activate(self):
        self.set_time()
        self.snooze_counter = 0
        self.enabled = True

    def deactivate(self):
        self.enabled = False
