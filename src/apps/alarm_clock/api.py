import uasyncio as asyncio

from uaos import App
from apps import apify


@apify.route("/alarm/all")
async def get_alarms(content):
    await asyncio.sleep(0)
    return App.get_app("AlarmClockApp").alarms
