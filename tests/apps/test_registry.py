import pytest

from django.apps import apps as django_apps

from reactor.apps.registry import Apps


@pytest.fixture(autouse=True)
def _django_apps_as_ready(mocker):
    mocker.patch.object(django_apps, "ready", True)


@pytest.fixture()
def make_app_config(mocker):
    def _make_app_config(name):
        app_config = mocker.Mock()

        app_config.name = name
        app_config.label = app_config.name.rpartition(".")[2]

        return app_config

    return _make_app_config


@pytest.fixture()
def make_model(mocker):
    def _make_model(app_label, model_name):
        model = mocker.Mock()

        model._meta = mocker.Mock(
            app_label=app_label,
            model_name=model_name.lower(),
            label=f"{app_label}.{model_name}",
        )

        return model

    return _make_model


def test_registry_is_populated_when_django_apps_ready(mocker):
    apps_populate = mocker.patch.object(Apps, "populate")

    Apps()

    apps_populate.assert_called()


def test_registry_is_not_populated_when_django_apps_not_ready(mocker):
    mocker.patch.object(django_apps, "ready", False)

    apps_populate = mocker.patch.object(Apps, "populate")

    Apps()

    apps_populate.assert_not_called()


def test_registry_contains_only_apps_installed_from_specified_packages(mocker, make_app_config):  # fmt: skip
    package_1_app_config = make_app_config("package_1.package_1_app")
    package_2_app_config = make_app_config("package_2.package_2_app")
    package_3_app_config = make_app_config("package_3.package_3_app")

    mocker.patch.object(
        django_apps,
        "app_configs",
        {
            "package_1_app": package_1_app_config,
            "package_2_app": package_2_app_config,
            "package_3_app": package_3_app_config,
        },
    )

    apps = Apps("package_1", "package_2")

    assert apps.app_configs == {
        "package_1_app": package_1_app_config,
        "package_2_app": package_2_app_config,
    }


def test_registry_get_app_configs_returns_all_registry_apps(mocker):
    apps = Apps()

    mocker.patch.object(apps, "app_configs")

    app_configs = apps.get_app_configs()

    assert app_configs == apps.app_configs.values()


def test_registry_get_app_config_returns_app_config_from_valid_app_label(mocker):
    apps = Apps()

    mocker.patch.object(apps, "app_configs", {"package_app": mocker.Mock()})

    app_config = apps.get_app_config("package_app")

    assert app_config == apps.app_configs["package_app"]


def test_registry_get_app_config_raises_lookup_error_from_nonexistent_app_label(mocker):
    apps = Apps()

    mocker.patch.object(apps, "app_configs", {"package_app": mocker.Mock()})

    with pytest.raises(
        LookupError, match="no installed app with label 'nonexistent_app'"
    ):
        apps.get_app_config("nonexistent_app")


def test_registry_get_models_returns_models_from_all_registry_app_configs(mocker):
    app_config_1 = mocker.Mock()
    app_config_1.get_models.return_value = [model_1 := mocker.Mock()]

    app_config_2 = mocker.Mock()
    app_config_2.get_models.return_value = [
        model_2 := mocker.Mock(),
        model_3 := mocker.Mock(),
    ]

    apps = Apps()

    mocker.patch.object(
        apps, "get_app_configs", return_value=[app_config_1, app_config_2]
    )

    models = apps.get_models()

    assert list(models) == [model_1, model_2, model_3]


def test_registry_get_model_returns_model_from_valid_model_name(mocker):
    model = mocker.Mock()

    class AppConfig(mocker.Mock):
        models = {"model": model}

        def get_model(self, model_name):
            return self.models[model_name]

    apps = Apps()

    mocker.patch.object(apps, "get_app_config", return_value=AppConfig())

    assert apps.get_model("package_app.model") == model


def test_registry_get_model_returns_model_from_unique_model_name(mocker, make_model):
    model = make_model("package_app", "Model")

    apps = Apps()

    mocker.patch.object(apps, "get_models", return_value=[model])

    assert apps.get_model("model") == model


def test_registry_get_model_raises_lookup_error_from_nonexistent_model_name(mocker):
    apps = Apps()

    mocker.patch.object(apps, "get_models", return_value=[])

    with pytest.raises(LookupError, match="no installed model with name 'model'"):
        apps.get_model("model")


def test_registry_get_model_raises_value_error_from_nonunique_model_name(mocker, make_model):  # fmt: skip
    model_1 = make_model("package_app_1", "Model")
    model_2 = make_model("package_app_2", "Model")

    apps = Apps()

    mocker.patch.object(apps, "get_models", return_value=[model_1, model_2])

    with pytest.raises(
        ValueError,
        match=(
            "a model with name 'model' found in multiple apps; use 'package_app_1.Model' "
            "or 'package_app_2.Model' to refer to a specific model"
        ),
    ):
        apps.get_model("model")
