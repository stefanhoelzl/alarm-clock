import ntp
import uasyncio as asyncio
import utime as time

from settings import TIME_ZONE
from alarm_clock import peripherials
from alarm_clock.tasks import time_update, alarm_handler, off_switch, snoozer
from alarm_clock.alarm import Alarm


ntp.settime(tz=TIME_ZONE)

l = time.localtime()
h = l[Alarm.HOUR]
m = l[Alarm.MINUTE] + 1
alarm = Alarm.activated(h, m, daylight_time=30, snooze_time=5)
print("Time to ring:", (alarm.time - time.time()))

loop = asyncio.get_event_loop()
loop.create_task(time_update())
loop.create_task(alarm_handler())
loop.create_task(off_switch())
loop.create_task(snoozer())
loop.run_forever()
loop.close()

peripherials.deinit()
