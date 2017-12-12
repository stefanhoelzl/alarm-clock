class Event:
    pass


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
    def __init__(self, time=0):
        super().__init__()
        self.time = time
