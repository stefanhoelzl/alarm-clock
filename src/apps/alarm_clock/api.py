import uasyncio as asyncio

from uaos import App
from apps import apify


@apify.route(b"/alarm/all")
async def get_alarms(content):
    return App.get_app("AlarmClockApp").as_dict()


@apify.route(b"/alarm/off")
async def off(content):
    App.get_app("AlarmClockApp").off()
    return b""


@apify.route(b"/alarm/snooze")
async def snooze(content):
    App.get_app("AlarmClockApp").snooze()
    return b""


@apify.route(b"/alarm/disable")
async def disable(aid):
    aid = int(aid)
    App.get_app("AlarmClockApp").alarms[aid].disable()
    return b""


@apify.route(b"/alarm/enable")
async def enable(aid):
    aid = int(aid)
    App.get_app("AlarmClockApp").alarms[aid].enable()
    return b""


@apify.route(b"/alarm/new")
async def new(dct):
    App.get_app("AlarmClockApp").create(**dct)
    return b""


@apify.route(b"/alarm/delete")
async def delete(aid):
    aid = int(aid)
    del App.get_app("AlarmClockApp").alarms[aid]
    return b""
