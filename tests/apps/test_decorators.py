from reactor.apps.decorators import on_ready


def test_on_ready_method_has_on_ready_attribute(mocker):
    class AppConfig(mocker.Mock):
        def regular_method(self):
            pass

        @on_ready()
        def on_ready_method(self):
            pass

    app_config = AppConfig()

    assert not hasattr(app_config.regular_method, "on_ready")
    assert hasattr(app_config.on_ready_method, "on_ready")
