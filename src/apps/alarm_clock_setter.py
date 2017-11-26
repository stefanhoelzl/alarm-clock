from uaos import App
import utime as time
from apps.alarm_clock.alarm import Alarm


class AlarmClockSetter(App):
    requires = ["AlarmClock"]

    def __init__(self):
        l = time.localtime()
        h = l[Alarm.HOUR]
        m = l[Alarm.MINUTE] + 1
        a = Alarm(h, m, daylight_time=30, snooze_time=10)
        print("Time to ring:", (a.time - time.time()))

AlarmClockSetter.register()

