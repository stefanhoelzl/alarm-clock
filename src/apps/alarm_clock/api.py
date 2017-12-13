import uasyncio as asyncio

from uaos import App
from apps import apify


@apify.route(b"/alarm/all")
async def get_alarms(content):
    ret = {}
    for aid, alarm in App.get_app("AlarmClockApp").alarms.items():
        ret[str(aid)] = alarm.as_dict()
    return ret
