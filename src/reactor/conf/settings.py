from pathlib import Path

import dj_database_url as db_url
from configurations import Configuration
from decouple import config

from django.db import DEFAULT_DB_ALIAS
from django.utils.translation import gettext_lazy as _

__all__ = ["CI", "Local"]

DB_ALIAS_ENVIRONMENT_VARIABLE = "DJANGO_DATABASE_ALIAS"

# Django settings & configurations
# https://docs.djangoproject.com/en/5.0/ref/settings/
# https://django-configurations.readthedocs.io/


class Common(Configuration):
    """Defines a configuration common to all environments."""

    # Paths

    PROJECT_DIR = Path(__file__).resolve().parents[1]

    BASE_DIR = PROJECT_DIR.parents[1]

    # Databases

    DATABASES = {}

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    # Apps & middleware

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # URLs

    ROOT_URLCONF = "reactor.conf.urls"

    # Template engines

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                PROJECT_DIR / "templates",
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Internationalization

    USE_I18N = True

    LANGUAGE_CODE = "en"

    LANGUAGES = [
        ("en", _("English")),
        ("pl", _("Polish")),
    ]

    LOCALE_PATHS = [
        PROJECT_DIR / "locale",
    ]

    # Timezone

    USE_TZ = True

    TIME_ZONE = "Europe/Warsaw"

    # Static files

    STATIC_URL = "static/"

    STATICFILES_DIRS = [
        PROJECT_DIR / "static",
    ]

    STATIC_ROOT = BASE_DIR / "assets"

    # Media

    MEDIA_URL = "media/"

    MEDIA_ROOT = BASE_DIR / "media"

    # Fixtures

    FIXTURE_DIRS = [
        PROJECT_DIR / "fixtures",
    ]

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

        # Override the default database.
        if DB_ALIAS := config(DB_ALIAS_ENVIRONMENT_VARIABLE, default=None):
            if DB_ALIAS not in cls.DATABASES:
                raise ValueError(f"no set-up database with an alias {DB_ALIAS!r}.")

            cls.DATABASES = {DEFAULT_DB_ALIAS: cls.DATABASES[DB_ALIAS]}
        else:
            # If the 'DB_ALIAS_ENVIRONMENT_VARIABLE' is left unspecified, the "dummy"
            # settings are used just to suppress the connection handler's "You must
            # define a 'default' database" error.
            cls.DATABASES = {
                DEFAULT_DB_ALIAS: {
                    "ENGINE": "django.db.backends.dummy",
                }
            }


class DebugMixin:
    """Enables debugging mode and applies debugging settings."""

    # Debugging mode

    DEBUG = True

    # Security

    SECRET_KEY = "django-insecure-secret-key"

    ALLOWED_HOSTS = ["*"]


class DebugToolbarMixin:
    """Installs and sets up the Django Debug Toolbar app."""

    # Security

    INTERNAL_IPS = ["127.0.0.1"]

    @classmethod
    def pre_setup(cls):
        super().pre_setup()

        # Apps & middleware

        cls.INSTALLED_APPS += ["debug_toolbar"]

        cls.MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


class Development(DebugMixin, Common):
    """Defines a configuration common to all development environments."""


class Local(DebugToolbarMixin, Development):
    """Defines a configuration for local development environments."""

    # Databases

    DATABASES = {
        "sqlite": db_url.parse("sqlite:///db.sqlite3"),
    }


class CI(Development):
    """Defines a configuration for continuous integration (CI) environments."""

    # Databases

    DATABASES = {
        "sqlite": db_url.parse("sqlite://:memory:"),
    }


class Tests(Development):
    """Defines a configuration for running tests."""

    # Apps & middleware

    INSTALLED_APPS = Common.INSTALLED_APPS + ["tests"]

    # Databases

    DATABASES = {
        "sqlite": db_url.parse("sqlite://:memory:"),
    }
