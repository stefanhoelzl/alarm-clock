from apps.alarm_clock.peripherials import Daylight, Indicator, Switch, SnoozeButton


class DaylightMock(Daylight):
    def __init__(self, kelvin=5300):
        self.rgb = Daylight.kelvin_to_rgb(kelvin)
        self.set(0)

    def set(self, i):
        r, g, b = tuple(map(lambda x: int(x*i), self.rgb))
daylight = DaylightMock()


class IndicatorMock(Indicator):
    def __init__(self):
        self.off()

    def on(self):
        pass

    def off(self):
        pass
indicator = IndicatorMock()


class SwitchMock(Switch):
    def __init__(self):
        self.pressed = False
switch = SwitchMock()


class SnoozeButtonMock(SnoozeButton):
    def __init__(self):
        pass

    @property
    def triggered(self):
        return False
snooze_button = SnoozeButtonMock()
