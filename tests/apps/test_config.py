import importlib

import pytest

from reactor import apps
from reactor.apps.decorators import on_ready


@pytest.fixture()
def app_config():
    class AppConfig(apps.AppConfig):
        def regular_method(self):
            pass

        @on_ready()
        def on_ready_method(self):
            pass

    return AppConfig(__name__, importlib.import_module(__name__))


def test_app_config_ready_calls_on_ready_method(mocker, app_config):
    on_ready_method = mocker.patch.object(
        app_config, "on_ready_method", spec=app_config.on_ready_method
    )

    app_config.ready()

    on_ready_method.assert_called()


def test_app_config_ready_does_not_call_regular_method(mocker, app_config):
    regular_method = mocker.patch.object(
        app_config, "regular_method", spec=app_config.regular_method
    )

    app_config.ready()

    regular_method.assert_not_called()
