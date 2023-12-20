import re
from itertools import chain

from django.apps import apps as django_apps
from django.utils.text import get_text_list

__all__ = ["apps"]


class Apps:
    """A thin wrapper around the `django.apps.registry.Apps` for managing a subset of
    apps installed from specified packages.
    """

    def __init__(self, *app_packages):
        self._app_packages = app_packages

        # Mapping of labels to the installed `AppConfig`.
        self.app_configs = {}

        # Populate the registry's app configs.
        if django_apps.ready:
            self.populate()

    def populate(self):
        """Populate the `app_configs` dict with app labels and app configs of the apps
        installed from the registry packages.
        """
        app_config_name_pattern = (
            rf"^({'|'.join(map(re.escape, self._app_packages))})(?:\.\w+)*$"
        )
        self.app_configs = {
            app_config.label: app_config
            for app_config in django_apps.get_app_configs()
            if re.match(app_config_name_pattern, app_config.name)
        }

    def get_app_configs(self):
        """Return an iterable of all the registered app configs."""
        return self.app_configs.values()

    def get_app_config(self, app_label):
        """Return an app config for the app label given or raise `LookupError` if no
        app with that label exists.
        """
        try:
            return self.app_configs[app_label]
        except KeyError as exc_info:
            raise LookupError(
                f"no installed app with label {app_label!r}"
            ) from exc_info

    def get_models(self):
        """Return an iterable of all the models defined in the registry's apps."""
        return chain(
            *[app_config.get_models() for app_config in self.get_app_configs()]
        )

    def get_model(self, model_name):
        """Return a model based on its (case insensitive) name.

        Compared to the "base" method of `django.apps.registry.apps`, a model can
        be returned based on its `model_name` meta-attribute only (the "base" method
        requires either a `app_label.model_name` label or `app_label` and `model_name`
        separately). If multiple models with the same names are found, a `ValueError`
        is raised.
        """
        if "." in model_name:
            app_label, model_name = model_name.split(".")

            return self.get_app_config(app_label).get_model(model_name)

        model_name = model_name.lower()
        if not (
            models := [
                model
                for model in self.get_models()
                if model._meta.model_name == model_name
            ]
        ):
            raise LookupError(f"no installed model with name {model_name!r}")

        if len(models) > 1:
            model_labels = get_text_list(
                [f"{model._meta.label!r}" for model in models], last_word="or"
            )
            raise ValueError(
                f"a model with name {model_name!r} found in multiple apps; use "
                f"{model_labels} to refer to a specific model"
            )

        return models[0]


apps = Apps("reactor")
