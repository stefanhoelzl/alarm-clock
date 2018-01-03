class EventHandler:
    def __init__(self, events, handler):
        self.events = events
        self.handler = handler


def event(*events):
    def decorator(event_handler):
        def wrapper(self, ev):
            new_state = event_handler(self, ev)
            if not new_state or type(self) == new_state:
                return None
            return new_state(self.state_machine)
        return EventHandler(events, wrapper)
    return decorator


class BaseState:
    def __call__(self, ev):
        return self


class State(BaseState):
    EventHandler = {}

    def __init__(self, sm):
        self.state_machine = sm
        self.register_event_handler()

    def register_event_handler(self):
        if self.__class__ not in State.EventHandler:
            State.EventHandler[self.__class__] = {}
            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if isinstance(attr, EventHandler):
                    for ev in attr.events:
                        State.EventHandler[self.__class__][ev] = attr.handler

    def __call__(self, ev):
        ret = State.EventHandler.get(self.__class__, {})\
                                .get(ev.__class__, lambda s, e: None)(self, ev)
        if ret is None:
            return super().__call__(event)
        elif not isinstance(ret, State):
            raise ValueError("State must return None or another state")
        return ret


class StateMachine:
    def __init__(self, initial_state):
        self.state = initial_state

    def transition(self, ev):
        new_state = self.state(ev)
        self.state = new_state

    def __eq__(self, other):
        return isinstance(self.state, other)
