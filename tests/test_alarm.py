import pytest
from unittest.mock import patch, PropertyMock

from alarm_clock.alarm import Alarm


def time(h, m):
    return ((h-1)*60 + m)*60


class TestAlarm:
    def test_daylight_onNoDaylightTime_noDaylight(self):
        alarm = Alarm()
        alarm.daylight_time = None
        assert alarm.daylight == 0

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=0)
    def test_daylight_onZeroTimeLeft_daylightFull(self, t):
        alarm = Alarm()
        alarm.enabled = True
        alarm.daylight_time = 1
        assert alarm.daylight == 1.0

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=10)
    def test_daylight_onTimeLeftGreaterDaylightTime_daylightZero(self, t):
        alarm = Alarm()
        alarm.daylight_time = 9.9
        assert alarm.daylight == 0.0

    def test_daylight_onTimeLeftBetweenDayligthTimeAnd0_daylightDim(self):
        alarm = Alarm()
        alarm.enabled = True
        alarm.daylight_time = 100
        for time_left in range(100, 0, -1):
            with patch(__name__ + '.Alarm.time_left',
                       new_callable=PropertyMock, return_value=time_left):
                assert alarm.daylight == (100-time_left)/100.0

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=0)
    def test_daylight_onDisabled_zero(self, t):
        alarm = Alarm()
        alarm.daylight_time = 1
        alarm.enabled = False
        assert alarm.daylight == 0.0

    @patch("time.time", return_value=0)
    def test_timeLeft_positive(self, time):
        alarm = Alarm()
        alarm.time = 100
        assert alarm.time_left == 100

    @patch("time.time", return_value=100)
    def test_timeLeft_zero(self, time):
        alarm = Alarm()
        alarm.time = 100
        assert alarm.time_left == 0

    @patch("time.time", return_value=200)
    def test_timeLeft_negative(self, time):
        alarm = Alarm()
        alarm.time = 100
        assert alarm.time_left == -100

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=1)
    def test_ringing_onTimeLeftGreaterZero_False(self, t):
        assert not Alarm().ringing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=0)
    def test_ringing_timeLeftIsZero_True(self, t):
        alarm = Alarm()
        alarm.enabled = True
        assert alarm.ringing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=-0.1)
    def test_ringing_timeLeftLessThanZero_True(self, t):
        alarm = Alarm()
        alarm.enabled = True
        assert alarm.ringing

    @patch("time.time", return_value=1)
    @patch(__name__ + '.Alarm.snoozing',
           new_callable=PropertyMock, return_value=True)
    def test_ringing_onSnoozing_False(self, t, s):
        alarm = Alarm()
        alarm.time = 0.5
        assert not alarm.ringing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=-0.1)
    def test_ringing_onDisabled_False(self, t):
        alarm = Alarm()
        alarm.enabled = False
        assert not alarm.ringing

    def test_snooze_increaseCounter(self):
        alarm = Alarm()
        alarm.snooze_counter = 45
        alarm.snooze()
        assert alarm.snooze_counter == 46

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=1.0)
    def test_snoozing_onTimeLeftPositive_False(self, t):
        alarm = Alarm()
        assert not alarm.snoozing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=0.0)
    def test_snoozing_onCounterZero_False(self, t):
        alarm = Alarm()
        alarm.snooze_counter = 0
        assert not alarm.snoozing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=-0.99)
    def test_snoozing_onCounterGreaterZeroAndTimeNotElapsed_True(self, t):
        alarm = Alarm()
        alarm.snooze_time = 1
        alarm.snooze_counter = 1
        assert alarm.snoozing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=-1.0)
    def test_snoozing_onCounterGreaterZeroAndTimeElapsed_False(self, t):
        alarm = Alarm()
        alarm.snooze_time = 1
        alarm.snooze_counter = 1
        assert not alarm.snoozing

    def test_off_setEnabled_False(self):
        alarm = Alarm()
        alarm.off()
        assert not alarm.enabled

    def test_off_onRepeating_activate(self):
        alarm = Alarm()
        alarm.days = (1,)
        alarm.enabled = True
        alarm.off()
        assert alarm.enabled

    def test_off_onRepeating_setTime(self):
        alarm = Alarm()
        alarm.days = (1, 2, 3)
        alarm.time = 60*60
        with patch(__name__ + ".Alarm.next_time", return_value=24*60*60):
            alarm.off()
        assert alarm.time == 24*60*60

    @patch("time.time", return_value=time(17, 0))
    def test_setTime_laterAtSameDay(self, t):
        alarm = Alarm()
        alarm.hour = 17
        alarm.minute = 10
        alarm.set_time()
        assert alarm.time == time(17, 10)

    @patch("time.time", return_value=time(17, 10))
    def test_setTime_nextDay(self, t):
        alarm = Alarm()
        alarm.hour = 17
        alarm.minute = 10
        alarm.set_time()
        assert alarm.time == time(24+17, 10)

    @patch("time.time", return_value=time(17, 10)+5)
    def test_setTime_secondsToZero(self, t):
        alarm = Alarm()
        alarm.hour = 17
        alarm.minute = 10
        alarm.set_time()
        assert alarm.time == time(24+17, 10)

    def test_activate_setEnabled(self):
        alarm = Alarm()
        alarm.enabled = False
        alarm.activate()
        assert alarm.enabled

    def test_activate_resetSnoozeCounter(self):
        alarm = Alarm()
        alarm.snooze_counter = 10
        alarm.activate()
        assert alarm.snooze_counter == 0

    @patch("time.time", return_value=0)
    def test_activate_setTime(self, t):
        alarm = Alarm()
        alarm.hour = 17
        alarm.minute = 10
        alarm.activate()
        assert alarm.time == time(17, 10)

    def test_deactivate_unsetEnabled(self):
        alarm = Alarm()
        alarm.enabled = True
        alarm.deactivate()
        assert not alarm.enabled

    def test_nextTime_returnTime_ifTimeWasNotReached(self):
        alarm = Alarm()
        alarm.time = 100
        alarm.days = (0,)
        with patch("time.time", return_value=0):
            assert alarm.next_time() == 100

    def test_nextTime_returnNone_ifNoneDays(self):
        alarm = Alarm()
        assert alarm.next_time() is None

    @pytest.mark.parametrize("current_day, days, day_diff", (
            # single day
            (0, (1,), 1),
            (1, (2,), 1),
            (6, (0,), 1),
            (0, (6,), 6),
            (4, (1,), 4),
            (6, (0,), 1),
            # multiple days
            (3, (1, 3, 4), 1),
            (4, (1, 4), 4),
            # unordered days
            (4, (4, 1), 4),
    ))
    def test_nextTime_onlyOneDayInSelection(self,
                                            current_day, days, day_diff):
        alarm = Alarm()
        alarm.hour = 10
        alarm.minute = 0
        alarm.days = days
        with patch("time.time", return_value=0):
            alarm.set_time()
        with patch("time.localtime",
                   return_value=(0, 0, 0, 10, 0, 0, current_day, 0)):
            assert alarm.next_time() == time(day_diff*24+10, 0)

    def test_diffBetweenWeekdays_withoutOverflow(self):
        assert Alarm.diff_between_weekdays(0, 2) == 2

    def test_diffBetweenWeekdays_withOverflow(self):
        assert Alarm.diff_between_weekdays(4, 1) == 4

    def test_getNextWeekday_singleValueInList(self):
        alarm = Alarm()
        alarm.days = (1,)
        assert alarm.get_next_weekday(2) == 1

    def test_getNextWeekday_multipleOrderedDays(self):
        alarm = Alarm()
        alarm.days = (1, 4)
        assert alarm.get_next_weekday(1) == 4

    def test_getNextWeekday_multipleOrderedDaysWithOverflow(self):
        alarm = Alarm()
        alarm.days = (1, 4)
        assert alarm.get_next_weekday(4) == 1

    def test_getNextWeekday_multipleUnorderedDays(self):
        alarm = Alarm()
        alarm.days = (4, 1, 3)
        assert alarm.get_next_weekday(3) == 4

    def test_getNextWeekday_multipleUnorderedDaysWithOverflow(self):
        alarm = Alarm()
        alarm.days = (4, 1, 3)
        assert alarm.get_next_weekday(4) == 1
