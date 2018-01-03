import time
from apps.ntp import NTP

LOCALTIME_IDX_YEAR = 0
LOCALTIME_IDX_MONTH = 1
LOCALTIME_IDX_DAY = 2
LOCALTIME_IDX_HOUR = 3
LOCALTIME_IDX_MINUTE = 4
LOCALTIME_IDX_SECOND = 5
LOCALTIME_IDX_WEEKDAY = 6
LOCALTIME_IDX_YEARDAY = 7


def next_time(hour, minute, days=None, current_time=None):
    if current_time is None:
        current_time = NTP.time()
    t = list(time.localtime(current_time))
    t[LOCALTIME_IDX_HOUR] = hour
    t[LOCALTIME_IDX_MINUTE] = minute
    t[LOCALTIME_IDX_SECOND] = 0
    at = time.mktime(tuple(t))
    if at <= current_time:
        t[LOCALTIME_IDX_DAY] += 1
        at = time.mktime(tuple(t))
    if days is not None:
        current_alarm_day = list(time.localtime(at))[LOCALTIME_IDX_WEEKDAY]
        if not (current_alarm_day in days and at > current_time):
            next_day = get_next_weekday(current_alarm_day, days)
            diff = diff_between_weekdays(current_alarm_day, next_day)
            t[LOCALTIME_IDX_DAY] += diff
            at = time.mktime(tuple(t))
    return at


def diff_between_weekdays(current, next):
    diff = next - current
    if diff < 0:
        diff = (next + 7) - current
    return diff


def get_next_weekday(current_day, days):
    for day in sorted(days):
        if day > current_day:
            return day
    return min(days)
