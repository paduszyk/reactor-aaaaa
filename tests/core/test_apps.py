import pytest

from django.conf import settings

from reactor.apps import apps


@pytest.mark.parametrize(
    "app_config_name",
    [
        app_config_name
        for app_config_name in settings.INSTALLED_APPS
        if app_config_name.startswith("reactor.")
    ],
)
def test_reactor_app_is_found_in_apps_registry(app_config_name):
    app_config_names = [app_config.name for app_config in apps.get_app_configs()]

    assert app_config_name in app_config_names
