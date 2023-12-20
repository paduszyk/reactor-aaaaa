from reactor import apps
from reactor.apps import apps as reactor_apps

__all__ = ["CoreConfig"]


class CoreConfig(apps.AppConfig):
    """Represents the `core` app and its configuration.

    Ensure this app is installed as the very first of the project's apps, as its
    `ready()` hook populates the app registry (see: `reactor.apps.registry.apps`).
    """

    name = "reactor.core"

    def ready(self):
        # Populate the project's apps registry, so that other apps and their
        # `@on_ready`-decorated hooks can use it.
        reactor_apps.populate()

        super().ready()
