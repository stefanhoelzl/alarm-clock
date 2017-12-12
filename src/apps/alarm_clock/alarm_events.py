class Event:
    def __init__(self, alarm):
        self.alarm = alarm


class Enable(Event):
    pass


class Disable(Event):
    pass


class Off(Event):
    pass


class Snooze(Event):
    pass


class DaylightOff(Event):
    pass


class Update(Event):
    pass
