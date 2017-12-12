from unittest.mock import patch
import pytest

from ..alarm import *


class TestInit:
    def test_stateIsEnabled(self):
        assert Alarm() == Enabled


class TestDaylight:
    def test_zero_ifStateNotDaylight(self):
        a = Alarm()
        assert a.daylight == 0

    def test_zero_ifDaylightButNoDaylightMode(self):
        a = Alarm(daylight_mode=False)
        a.state = Daylight(a)
        assert a.daylight == 0

    def test_zero_ifDaylightButTimeNotReached(self):
        a = Alarm(daylight_mode=True, daylight_time=10)
        a.state = Daylight(a)
        a.time = 110
        with patch("time.time", return_value=100):
            assert a.daylight == 0

    def test_rampUp(self):
        a = Alarm(daylight_mode=True, daylight_time=100)
        a.state = Daylight(a)
        a.time = 100
        for i in range(100):
            with patch("time.time", return_value=i):
                assert a.daylight == i/100.0

    def test_saturateAtOne(self):
        a = Alarm(daylight_mode=True, daylight_time=50)
        a.state = Daylight(a)
        a.time = 100
        with patch("time.time", return_value=200):
            assert a.daylight == 1.0


@pytest.mark.parametrize("state, ringing", (
        (Disabled, False),
        (Enabled, False),
        (Daylight, False),
        (Ringing, True),
        (Snoozing, False),
))
def test_ringing(state, ringing):
    a = Alarm()
    a.state = state(a)
    assert a.ringing == ringing


@pytest.mark.parametrize("state, snoozing", (
        (Disabled, False),
        (Enabled, False),
        (Daylight, False),
        (Ringing, False),
        (Snoozing, True),
))
def test_snoozing(state, snoozing):
    a = Alarm()
    a.state = state(a)
    assert a.snoozing == snoozing
