import os
import sys
from pathlib import Path

from decouple import config
from dotenv import load_dotenv

__all__ = []


def main():
    """Set up Django and run a management command.

    Configured using `django-configurations`.

    See: https://django-configurations.readthedocs.io/.
    """
    # Load environment variables from '.env' if the project is run locally.
    CI = config("CI", cast=bool, default=False)
    if not CI:
        load_dotenv()

    # Load IPython profile if shell is requested.
    if sys.argv[1] == "shell":
        os.environ.setdefault(
            "IPYTHONDIR", (Path(__file__).resolve().parent / ".ipython").as_posix()
        )

    try:
        from configurations.management import execute_from_command_line
    except (ImportError, ModuleNotFoundError) as exc_info:
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured(
            "'configurations' package is not installed"
        ) from exc_info

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
