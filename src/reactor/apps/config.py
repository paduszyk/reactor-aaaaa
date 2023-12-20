from django import apps

__all__ = ["AppConfig"]


class AppConfig(apps.AppConfig):
    """Represents a base for configuration classes of the project's apps."""
