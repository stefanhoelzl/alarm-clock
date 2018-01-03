from .dependency_resolver import resolve_dependencies


class AppServer:
    __registered__ = {}

    missing_requirements = {}
    initialized = []
    init_failed = {}
    running = []
    broken = {}
    finished = []

    __execution_order__ = []

    @staticmethod
    def setup():
        order, unresolved, unfulfilled = \
            resolve_dependencies(AppServer.__registered__)
        AppServer.__execution_order__ = order
        for app_name in AppServer.__execution_order__:
            AppServer.setup_app(app_name)

    @staticmethod
    def setup_app(app_name):
        try:
            app = AppServer.__registered__[app_name]
            app["instance"] = app["cls"]()
            AppServer.initialized.append(app_name)
        except Exception as e:
            print("init failed", app_name, e)
            AppServer.init_failed[app_name] = e

    @staticmethod
    async def call_safe(app_name, task):
        while True:
            try:
                AppServer.running.append(app_name)
                print("started", app_name)
                await task()
            except Exception as e:
                print("broken", app_name, e)
                AppServer.broken[app_name] = e
            else:
                print("finished", app_name)
                AppServer.finished.append(app_name)
                break
            finally:
                AppServer.running.remove(app_name)

    @staticmethod
    def start(loop):
        for app_name in AppServer.__execution_order__:
            infos = AppServer.__registered__[app_name]
            if hasattr(infos["instance"], '__call__'):
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
    def register(cls):
        AppServer.__registered__[cls.__name__] = {
            "cls": cls,
            "instance": None
        }

    @staticmethod
    def get_app(app):
        return AppServer.__registered__[app]["instance"]
