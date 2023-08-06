# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Console script for python-active-versions."""

import inspect
import types
from typing import Any, Callable, TypeVar, cast

import click
from cloup import HelpFormatter, HelpTheme, Style, option, option_group

from python_active_versions import __version__
from python_active_versions.python_active_versions import get_active_python_versions
from python_active_versions.utility import configure_logger

F = TypeVar('F', bound=Callable[..., Any])

formatter_settings = HelpFormatter.settings(
    theme=HelpTheme(
        invoked_command=Style(fg='bright_yellow'),
        heading=Style(fg='bright_white', bold=True),
        constraint=Style(fg='magenta'),
        col1=Style(fg='bright_yellow'),
    )
)


@click.command()
@option_group(
    "Generic Options",
    option(
        '-l',
        '--loglevel',
        'loglevel',
        type=click.Choice(["debug", "info", "warning", "error"], case_sensitive=False),
        default="warning",
        show_default=True,
        help="set log level",
    ),
)
@option_group(
    "Docker",
    option(
        '-d',
        '--docker',
        'docker',
        is_flag=True,
        type=click.BOOL,
        default=False,
        show_default=True,
        help="Get Docker image info.",
    ),
)
@click.version_option(__version__)
def get_python_versions(loglevel: str, docker: bool):
    """Python extension for Code128 barcode generator library cli script.

    Arguments:
        loglevel: set log level.
        docker: Include also info coming from docker's python active images.
    """
    _fnc_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
    _complete_doc = inspect.getdoc(eval(_fnc_name))  # pylint: disable=eval-used  # nosec B307
    _doc = f"{_complete_doc}".split('\n')[0]  # use only doc first row
    _str = f"{_doc[:-1]} - v{__version__}"
    click.echo(f"{_str}")
    click.echo("=" * len(_str))

    configure_logger(loglevel)

    click.echo("\nPython version found:")
    for _v in get_active_python_versions(docker, loglevel):
        click.echo(f"  Version: {_v['version']}")
        click.echo(f"  Latest Software Version: {_v['latest_sw']}")
        if 'docker_images' in _v and _v['docker_images']:
            click.echo('  Docker images:')
            _spaced = list(map(lambda x: f"    {x}", _v['docker_images']))
            click.echo("\n".join(_spaced))

        click.echo("-" * len(_str))


if __name__ == "__main__":
    get_python_versions()  # pragma: no cover  # pylint: disable=no-value-for-parameter
