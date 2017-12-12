import pytest

from ..state_machine import StateMachine, State, event


class StateMock:
    def __init__(self):
        self.event = False

    def __call__(self, ev):
        self.event = ev


class TestStateMachine:
    def test_transition_callStateWithEvent(self):
        state = StateMock()
        sm = StateMachine(state)
        sm.transition("Event")
        assert state.event == "Event"

    def test_eq_StateType(self):
        sm = StateMachine(StateMock())
        assert sm == StateMock


class TestState:
    def test_registerEventHandler(self):
        class StateWithEvents(State):
            @event(str, int)
            def bla(self, ev):
                return lambda x: "TEST_" + ev

            @event(float)
            def f(self, ev):
                return lambda x: "TEST2_" + ev

        s = StateWithEvents(None)
        assert StateWithEvents in State.EventHandler
        assert str in State.EventHandler[StateWithEvents]
        assert int in State.EventHandler[StateWithEvents]
        assert float in State.EventHandler[StateWithEvents]
        assert State.EventHandler[StateWithEvents][str](s, "STR") == "TEST_STR"
        assert State.EventHandler[StateWithEvents][int](s, "INT") == "TEST_INT"
        assert State.EventHandler[StateWithEvents][float](s, "FL") == "TEST2_FL"

    def test_call(self):
        class ParentState(State):
            @event(str)
            def str_(self, ev):
                return State

        class SubState(ParentState):
            @event(int)
            def int_(self, ev):
                return ParentState

        s = SubState(None)(1)
        assert type(s) == ParentState

        s = SubState(None)("test")
        assert type(s) == State

        s = SubState(None)
        s_new = s(object())
        assert s is s_new

    def test_raiseValueError_onEventHandlerReturnsNotState(self):
        class WrongState(State):
            @event(str)
            def wrong(self, ev):
                return str

        s = WrongState(None)
        with pytest.raises(ValueError):
            s("test")
