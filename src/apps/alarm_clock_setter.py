from uaos import App
import utime as time
import uasyncio as asyncio


class AlarmClockSetter(App):
    requires = ["AlarmClockApp"]

    def __init__(self):
        l = time.localtime()
        h = l[3]
        m = l[4] + 1
        alarm_clock = self.get_app("AlarmClockApp")
        alarm_clock.create(h, m, dl_time=50, dl_mode=True, snooze=10)

    async def __call__(self):
        await asyncio.sleep(65)
        self.get_app("AlarmClockApp").off()

AlarmClockSetter.register()

