from django import apps

from .decorators import on_ready

__all__ = ["AppConfig"]


class AppConfig(apps.AppConfig):
    """Represents a base for configuration classes of the project's apps."""

    def ready(self):
        super().ready()

        # Call all the `@on_ready`-decorated methods.
        for method in [
            attr
            for attr_name in dir(self)
            if callable(attr := getattr(self, attr_name))
        ]:
            if getattr(method, on_ready.__name__, False):
                method()
