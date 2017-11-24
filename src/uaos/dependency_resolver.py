class DependencyResolver:
    def __init__(self, apps):
        self.apps = apps
        self.app_list = list(apps.keys())
        self.app_list.sort()
        self.order = []
        self.unresolvable = {}
        self.unfulfilled = {}
        self.deps = {}

    def app_is_resolved(self, app_name):
        if app_name in self.order:
            return True
        if app_name in self.unresolvable:
            return True
        if app_name in self.unfulfilled:
            return True
        return False

    def app_dependencies_are_registered(self, app_name):
        return app_name in self.deps

    def unresolved_dependencies(self, app_name):
        return [(a, t) for (a, t) in self.deps.get(app_name, [])
                if a not in self.order]

    def register_app_dependencies(self, app_name):
        app = self.apps[app_name]["cls"]
        requires = tuple(((r, True) for r in app.requires))
        optional = tuple(((r, False) for r in app.optional))
        self.deps[app_name] = [(a, t) for (a, t) in
                               requires + optional
                               if a not in self.order]

    def app_has_no_pending_dependencies(self, app_name):
        return not self.deps[app_name] \
               and not len(self.unresolvable.get(app_name, []))

    def handle_undone_dependencies(self, app_name):
        if app_name in self.deps and self.deps[app_name]:
            self.unresolvable[app_name] = [a for (a, r) in self.deps[app_name]
                                           if r]
            self.unfulfilled[app_name] = [a for (a, r) in self.deps[app_name]
                                          if not r]
            if not self.unfulfilled[app_name]:
                del self.unfulfilled[app_name]
            if not self.unresolvable[app_name]:
                del self.unresolvable[app_name]
        self.deps[app_name] = None

    def resolve(self):
        changed = True
        handle_undone_dependencies = False
        while changed or handle_undone_dependencies:
            changed = False
            for app_name in self.app_list:
                if not self.app_is_resolved(app_name):
                    if not self.app_dependencies_are_registered(app_name):
                        changed = True
                        self.register_app_dependencies(app_name)
                    else:
                        self.deps[app_name] = self.unresolved_dependencies(
                            app_name
                        )
                    if self.app_has_no_pending_dependencies(app_name):
                        self.order.append(app_name)
                        changed = True
                if not changed and handle_undone_dependencies:
                    self.handle_undone_dependencies(app_name)
            if not changed and not handle_undone_dependencies:
                handle_undone_dependencies = True
            elif handle_undone_dependencies:
                return


def resolve_dependencies(apps):
    resolver = DependencyResolver(apps)
    resolver.resolve()
    return resolver.order, resolver.unresolvable, resolver.unfulfilled