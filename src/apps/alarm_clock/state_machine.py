class EventHandler:
    def __init__(self, events, handler):
        self.events = events
        self.handler = handler


def event(*events):
    def decorator(event_handler):
        return EventHandler(events, event_handler)
    return decorator


class BaseState:
    def __call__(self, event):
        return self


class State(BaseState):
    EventHandler = {}

    def __init__(self):
        self.register_event_handler()

    def register_event_handler(self):
        if self.__class__ not in State.EventHandler:
            State.EventHandler[self.__class__] = {}
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if isinstance(attr, EventHandler):
                    for event in attr.events:
                        State.EventHandler[self.__class__][event] = attr.handler

    def __call__(self, event):
        ret = None
        if self.__class__ in State.EventHandler:
            if event.__class__ in State.EventHandler[self.__class__]:
                ret = State.EventHandler[self.__class__][event.__class__](self,
                                                                          event)
        if ret:
            return ret
        return super().__call__(event)


class StateMachine:
    def __init__(self):
        self.state = None

    def transition(self, e):
        self.state = self.state(e)

    def __eq__(self, other):
        return isinstance(self, other)
