from uaos import App
import time
from apps.ntp import NTP


class AlarmClockSetter(App):
    requires = ["AlarmClockApp"]

    def __init__(self):
        t = NTP.time()
        l = time.localtime(t)
        h = l[3]
        m = l[4] + 10
        alarm_clock = self.get_app("AlarmClockApp")

        # alarm_clock.create(h, m,
        #                    daylight_time=10*60, daylight_mode=True,
        #                    snooze_time=10)

        alarm_clock.create(7, 0, days=(0, 1, 2, 3, 4),
                           daylight_time=30*60, daylight_mode=True,
                           snooze_time=0, enabled=True)

AlarmClockSetter.register()

