from unittest.mock import patch, PropertyMock

from alarm_clock.alarm import Alarm


class TestAlarm:
    def test_daylight_onNoDaylightTime_noDaylight(self):
        alarm = Alarm()
        alarm.daylight_time = None
        assert alarm.daylight == 0

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=0)
    def test_daylight_onZeroTimeLeft_daylightFull(self, t):
        alarm = Alarm()
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
        assert Alarm().ringing

    @patch(__name__ + '.Alarm.time_left',
           new_callable=PropertyMock, return_value=-0.1)
    def test_ringing_timeLeftLessThanZero_True(self, t):
        assert Alarm().ringing

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

    @patch("time.time", return_value=(16*60)*60)
    def test_setTime_laterAtSameDay(self, t):
        alarm = Alarm()
        alarm.hour = 17
        alarm.minute = 10
        alarm.set_time()
        assert alarm.time == (16*60+10)*60

    @patch("time.time", return_value=(16*60+11)*60)
    def test_setTime_nextDay(self, t):
        alarm = Alarm()
        alarm.hour = 17
        alarm.minute = 10
        alarm.set_time()
        assert alarm.time == ((24+16)*60+10)*60

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
        assert alarm.time == (16*60+10)*60

    def test_deactivate_unsetEnabled(self):
        alarm = Alarm()
        alarm.enabled = True
        alarm.deactivate()
        assert not alarm.enabled
