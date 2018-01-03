import pytest
from unittest.mock import patch

from ..alarm_time import diff_between_weekdays, get_next_weekday, next_time


# time.localtime(126000) 35*60*60
# time.struct_time(tm_year=1970, tm_mon=1, tm_mday=2,
#                  tm_hour=12, tm_min=0, tm_sec=0,
#                  tm_wday=4, tm_yday=2, tm_isdst=0)
def time_(hours=0, minutes=0):
    return 126000 + (hours * 60 + minutes) * 60


class TestDiffBetweenWeekdays:
    @pytest.mark.parametrize("current, next, diff", (
            (0, 1, 1),
            (0, 0, 0),
            (6, 0, 1),
            (6, 6, 0),
    ))
    def test_allDays(self, current, next, diff):
        assert diff_between_weekdays(current, next) == diff


class TestGetNextWeekday:
    def test_singleValueInList(self):
        assert get_next_weekday(2, (1,)) == 1

    def test_multipleOrderedDays(self):
        assert get_next_weekday(1, (1, 4)) == 4

    def test_multipleOrderedDaysWithOverflow(self):
        assert get_next_weekday(4, (1, 4)) == 1

    def test_multipleUnorderedDays(self):
        assert get_next_weekday(3, (4, 1, 3)) == 4

    def test_multipleUnorderedDaysWithOverflow(self):
        assert get_next_weekday(4, (4, 1, 3)) == 1


class TestNextTime:
    def test_sameDay_later(self):
        assert next_time(13, 0, current_time=time_()) == time_(1, 0)

    def test_sameDay_later_withDays(self):
        nt = next_time(13, 0, days=(0, 1, 2, 3, 4, 5, 6), current_time=time_())
        assert nt == time_(1, 0)

    def test_sameDay_earlier_getsNextDay(self):
        assert next_time(11, 0, current_time=time_()) == time_(23, 0)

    def test_days(self):
        assert next_time(12, 0, days=(6,), current_time=time_()) == time_(48, 0)
