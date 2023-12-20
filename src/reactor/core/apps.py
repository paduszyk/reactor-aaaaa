from reactor import apps

__all__ = ["CoreConfig"]


class CoreConfig(apps.AppConfig):
    """Represents the `core` app and its configuration."""

    name = "reactor.core"
