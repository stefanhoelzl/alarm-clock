def resolve_dependencies(apps):
    order = []
    unresolvable = {}
    unfulfilled = {}

    deps = {}

    repeat = True
    while repeat:
        repeat = False
        for app_name, info in apps.items():
            if app_name not in order and app_name not in unresolvable:
                if app_name not in deps:
                    app = info["cls"]
                    requires = tuple(((r, True) for r in app.requires))
                    optional = tuple(((r, False) for r in app.optional))
                    deps[app_name] = [(a, t) for (a, t) in requires + optional
                                      if a not in order]
                else:
                    unresolved = [(a, t)
                                  for (a, t) in deps.get(app_name, [])
                                  if a not in order]
                    if unresolved == deps[app_name]:
                        unresolvable[app_name] = [a for (a, r) in deps[app_name]
                                                  if r]
                        unfulfilled[app_name] = [a for (a, r) in deps[app_name]
                                                 if not r]
                        if not unfulfilled[app_name]:
                            del unfulfilled[app_name]
                        deps[app_name] = None
                    else:
                        deps[app_name] = unresolved
                if not deps[app_name] and not len(unresolvable.get(app_name,
                                                                   [])):
                    order.append(app_name)
                else:
                    repeat = True
    return order, unresolvable, unfulfilled


class AppServer:
    __registered__ = {}

    missing_requirements = {}
    initialized = []
    init_failed = {}
    running = []
    broken = {}
    finished = []
    pending = []

    __execution_order__ = []

    @staticmethod
    def setup():
        order, unresolved, unfulfilled = \
            resolve_dependencies(AppServer.__registered__)
        AppServer.__execution_order__ = order
        for app_name in AppServer.__execution_order__:
            try:
                app = AppServer.__registered__[app_name]
                app["instance"] = app["cls"]()
                AppServer.initialized.append(app_name)
            except Exception as e:
                AppServer.init_failed[app_name] = e
        print(AppServer.initialized)

    @staticmethod
    async def call_safe(app_name, task):
        try:
            AppServer.pending.remove(app_name)
            AppServer.running.append(app_name)
            print("started", app_name)
            await task()
        except Exception as e:
            print("broken", app_name, e)
            AppServer.broken[app_name] = e
        else:
            print("finished", app_name)
            AppServer.finished.append(app_name)
        finally:
            AppServer.running.remove(app_name)

    @staticmethod
    def start(loop):
        for app_name in AppServer.__execution_order__:
            infos = AppServer.__registered__[app_name]
            if hasattr(infos["instance"], '__call__'):
                AppServer.pending.append(app_name)
                loop.create_task(
                    AppServer.call_safe(
                        app_name, infos["instance"]
                    )
                )


class App:
    requires = []
    optional = []
    not_mandatory = False

    @classmethod
    def dependencies(cls):
        return tuple(((r, True) for r in cls.requires)) \
               + tuple(((r, False) for r in cls.optional))

    @classmethod
    def register(cls):
        AppServer.__registered__[cls.__name__] = {
            "cls": cls,
            "instance": None
        }
