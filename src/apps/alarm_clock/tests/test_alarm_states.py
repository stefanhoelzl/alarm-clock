from unittest.mock import patch

import collections

from apps.alarm_clock import alarm_events as events
from ..alarm_states import *


Transition = collections.namedtuple("Transition", "event sm state")


class AlarmMock:
    def __init__(self, hour=0, minute=0, days=None,
                 dl_mode=None, dl_time=0,
                 time=None, time_left=0,
                 snooze_time=0, snooze_counter=0, snooze_until=0):
        self.hour = hour
        self.minute = minute
        self.days = days
        self.daylight_time = dl_time
        self.time = time
        self.time_left = time_left
        self.daylight_mode = dl_mode
        self.snooze_time = snooze_time
        self.snooze_counter = snooze_counter
        self.snooze_until = snooze_until


class StateTest:
    State = State
    ExpectedTransitions = ()

    @property
    def state_machine(self):
        return AlarmMock()

    def unexpected_events(self):
        expected_events = tuple(set(type(t.event)
                                    for t in self.ExpectedTransitions))
        all_events = tuple(getattr(events, e) for e in dir(events)
                           if hasattr(getattr(events, e), "__bases__")
                           and Event in getattr(events, e).__bases__)
        for ev in all_events:
            for eev in expected_events:
                if ev == eev or eev in ev.__subclasses__():
                    break
            else:
                yield ev

    def test_expected_transitions(self):
        for trans in self.ExpectedTransitions:
            s = self.State(self.state_machine)
            s.alarm = trans.sm
            if trans.state:
                assert type(s(trans.event)) == trans.state
            else:
                assert s(trans.event) == s

    def test_unexpectedEvents_keepState(self):
        for ev in self.unexpected_events():
            s = self.State(self.state_machine)
            assert s(ev()) == s


class TestDisabled(StateTest):
    State = Disabled
    ExpectedTransitions = (
        Transition(Enable(), AlarmMock(), Enabled),
    )

    def test_setTimeToNone(self):
        s = self.State(AlarmMock())
        assert s.alarm.time is None


class TestEnabled(StateTest):
    State = Enabled
    ExpectedTransitions = (
        Transition(Disable(), AlarmMock(), Disabled),
        Transition(Update(100), AlarmMock(time=101), None),
        Transition(Update(99), AlarmMock(time=100, dl_time=1, dl_mode=True),
                   Daylight),
        Transition(Update(98), AlarmMock(time=99, dl_time=2, dl_mode=True),
                   Daylight),
        Transition(Update(98), AlarmMock(time=100, dl_time=1, dl_mode=True),
                   None),
        Transition(Update(100), AlarmMock(time=100, dl_time=1), Ringing),
        Transition(Update(101), AlarmMock(time=100, dl_time=1), Ringing),
    )

    def test_resetSnoozeCounter(self):
        s = self.State(AlarmMock(snooze_counter=100))
        assert s.alarm.snooze_counter == 0

    def test_setTimeToNextTime(self):
        a = AlarmMock(hour=2, time=0)
        s = self.State(a)
        assert s.alarm.time == 3600

    @patch("time.time", return_value=0)
    def test_setTimeFromNow(self, t):
        a = AlarmMock(hour=2)
        s = self.State(a)
        assert s.alarm.time == 3600


class TestDaylight(StateTest):
    State = Daylight
    ExpectedTransitions = (
        Transition(Disable(), AlarmMock(), Disabled),
        Transition(Off(), AlarmMock(), Disabled),
        Transition(Off(), AlarmMock(days=(1,)), Enabled),
        Transition(Update(100), AlarmMock(time=100), Ringing),
        Transition(Update(101), AlarmMock(time=100), Ringing),
    )

    @property
    def state_machine(self):
        return AlarmMock(time=0)


class TestRinging(StateTest):
    State = Ringing
    ExpectedTransitions = (
        Transition(Disable(), AlarmMock(), Disabled),
        Transition(Off(), AlarmMock(), Disabled),
        Transition(Off(), AlarmMock(days=(1,)), Enabled),
        Transition(Snooze(), AlarmMock(snooze_time=1), Snoozing),
    )

    @property
    def state_machine(self):
        return AlarmMock(time=0)


class TestSnoozing(StateTest):
    State = Snoozing
    ExpectedTransitions = (
        Transition(Disable(), AlarmMock(), Disabled),
        Transition(Off(), AlarmMock(), Disabled),
        Transition(Off(), AlarmMock(days=(2,)), Enabled),
        Transition(Update(99), AlarmMock(snooze_until=100), None),
        Transition(Update(100), AlarmMock(snooze_until=100), Ringing),
        Transition(Update(101), AlarmMock(snooze_until=100), Ringing),
    )

    @property
    def state_machine(self):
        return AlarmMock(time=0)

    def test_incSnoozeCounter(self):
        a = AlarmMock(snooze_counter=100, time=0)
        self.State(a)
        assert a.snooze_counter == 101

    def test_calcSnoozeUntil(self):
        a = AlarmMock(snooze_time=10, time=0)
        self.State(a)
        assert a.snooze_until == 10
