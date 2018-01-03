import pytest
from unittest.mock import patch

from ..api import *
from ..alarm import Alarm
from .. import AlarmClockApp
from ..alarm_states import Disabled, Enabled


class AlarmClockMock(AlarmClockApp):
    auto_store = False

    def __init__(self, alarms=None, off=False, snooze=False):
        super().__init__()
        self.alarms = alarms if alarms is not None else {}
        self._off = off
        self._snooze = snooze

    def off(self):
        self._off = True

    def snooze(self):
        self._snooze = True


@pytest.mark.asyncio
async def test_getAlarms():
    aid = 123
    alarm = Alarm(h=7, m=35, days=(1, 2), snooze_time=50,
                  daylight_mode=True, daylight_time=10)
    with patch("uaos.App.get_app", return_value=AlarmClockMock({aid: alarm})):
        alarms = (await get_alarms(""))
    assert alarms[0]['aid'] == 0
    assert alarms[0]['hour'] == 7
    assert alarms[0]['minute'] == 35
    assert alarms[0]['days'] == (1,2)
    assert alarms[0]['daylight_mode'] == True
    assert alarms[0]['daylight_time'] == 10
    assert alarms[0]['snooze_time'] == 50
    assert alarms[0]['daylight'] == 0
    assert alarms[0]['ringing'] is False
    assert alarms[0]['snoozing'] is False


@pytest.mark.asyncio
async def test_off():
    ac = AlarmClockMock()
    with patch("uaos.App.get_app", return_value=ac):
        await off("")
    assert ac.off


@pytest.mark.asyncio
async def test_snooze():
    ac = AlarmClockMock()
    with patch("uaos.App.get_app", return_value=ac):
        await snooze("")
    assert ac.snooze


@pytest.mark.asyncio
async def test_disable():
    ac = AlarmClockMock({123: Alarm()})
    assert ac.alarms[123] == Enabled
    with patch("uaos.App.get_app", return_value=ac):
        await disable("123")
    assert ac.alarms[123] == Disabled


@pytest.mark.asyncio
async def test_enable():
    ac = AlarmClockMock({123: Alarm()})
    ac.alarms[123].disable()
    assert ac.alarms[123] == Disabled
    with patch("uaos.App.get_app", return_value=ac):
        await enable("123")
    assert ac.alarms[123] == Enabled


@pytest.mark.asyncio
async def test_new():
    ac = AlarmClockMock()
    with patch("uaos.App.get_app", return_value=ac):
        await new({"hour": 7,
                   "minute": 24,
                   "days": (1, 2, 3),
                   "daylight_mode": True,
                   "daylight_time": 120,
                   "snooze_time": 60
                   })

    assert ac.alarms[0] == Enabled
    assert ac.alarms[0].hour == 7
    assert ac.alarms[0].minute == 24
    assert ac.alarms[0].days == (1, 2, 3)
    assert ac.alarms[0].daylight_mode == True
    assert ac.alarms[0].daylight_time == 120
    assert ac.alarms[0].snooze_time == 60


@pytest.mark.asyncio
async def test_delete():
    ac = AlarmClockMock({123: Alarm()})
    with patch("uaos.App.get_app", return_value=ac):
        await delete("123")
    assert 123 not in ac.alarms
