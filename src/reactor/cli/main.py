import importlib

import click
import configurations
from decouple import config
from dotenv import load_dotenv

from django.conf import settings

__all__ = ["reactor_cli"]


@click.group(
    name="reactor-cli",
    help="Run CLI utilities of the 'reactor' package.",
)
@click.version_option(
    package_name="reactor",
    message="%(version)s",
)
@click.pass_context
def reactor_cli(context):
    # Ensure that the entry point's context object is defined.
    context.ensure_object(dict)

    # Load environment variables from '.env' if the project is run locally.
    CI = config("CI", cast=bool, default=False)
    if not CI:
        load_dotenv()

    # Configure the project.
    configurations.setup()

    # Pass the projects' settings to the CLI context.
    context.obj["settings"] = settings


# Add commands defined in the '.commands' module.
commands_module = importlib.import_module("reactor.cli.commands")

for command in commands_module.__dict__.values():
    if isinstance(command, click.Command):
        reactor_cli.add_command(command)

if __name__ == "__main__":
    reactor_cli()
