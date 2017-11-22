import pytest
from uaos.app import App, resolve_dependencies


class AppMock:
    def __init__(self, requires=(), optional=()):
        self.requires = list(requires)
        self.optional = list(optional)


def MakeApp(name, **kwargs):
    cls = type(name, (App,), kwargs)
    return {
        "cls": cls,
        "instance": cls()
    }


def create_app_register(apps):
    register = {}
    for app_def in apps:
        app, defs = app_def
        register[app] = MakeApp(app, **defs)
    return register


class TestResolveDependencies:
    def test_oneWithoutDependendies(self):
        register = create_app_register((("App", {}),))
        order, r, o = resolve_dependencies(register)
        assert "App" in order

    def test_mulipleWithoutDependendies(self):
        register = create_app_register((("App1", {}), ("App2", {})))
        order, r, o = resolve_dependencies(register)
        assert "App1" in order
        assert "App2" in order

    def test_withDependencies_addToList(self):
        register = create_app_register((("App1", {}),
                                        ("App2", {"requires": ["App1"]})))
        order, r, o = resolve_dependencies(register)
        assert "App1" in order
        assert "App2" in order

    def test_withDeps_correctOrder(self):
        register = create_app_register((("App1", {}),
                                        ("App2", {"requires": ["App1"]})))
        order, r, o = resolve_dependencies(register)
        assert order.index("App1") < order.index("App2")

    def test_nestedDeps_allInList(self):
        register = create_app_register((("App1", {}),
                                        ("App2", {"requires": ["App1"]}),
                                        ("App3", {"requires": ["App2"]})))
        order, r, o = resolve_dependencies(register)
        assert "App1" in order
        assert "App2" in order
        assert "App3" in order

    def test_markAsUnresolved_ifDepsNotPresent(self):
        register = create_app_register((("App1", {}),
                                        ("App3", {"requires": ["App2"]})))
        order, unresolved, o = resolve_dependencies(register)
        assert "App1" in order
        assert "App3" in unresolved

    def test_notInOrder_ifDepsNotPresent(self):
        register = create_app_register((("App1", {}),
                                        ("App3", {"requires": ["App2"]})))
        order, unresolved, o = resolve_dependencies(register)
        assert "App3" not in order

    def test_markAsUnfulfilled_ifDepsNotPresent(self):
        register = create_app_register((("App1", {}),
                                        ("App3", {"optional": ["App2"]})))
        order, r, unfulfilled = resolve_dependencies(register)
        assert "App1" in order
        assert "App3" in unfulfilled

    def test_circularDeps(self):
        register = create_app_register((("App1", {"requires": ["App2"]}),
                                        ("App2", {"requires": ["App3"]}),
                                        ("App3", {"requires": ["App1"]})))
        order, unresolved, unfulfilled = resolve_dependencies(register)
        assert len(order) == 0
        assert len(unresolved) == 3
        assert "App1" in unresolved
        assert "App2" in unresolved
        assert "App3" in unresolved
