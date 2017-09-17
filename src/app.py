import ntp
import uasyncio as asyncio
import utime as time

from settings import TIME_ZONE
from alarm_clock import peripherials
from alarm_clock.tasks import time_update, alarm

ntp.settime(tz=TIME_ZONE)

loop = asyncio.get_event_loop()
loop.create_task(time_update())
loop.create_task(alarm(time.time()+15, 10))
loop.run_forever()
loop.close()

peripherials.deinit()
