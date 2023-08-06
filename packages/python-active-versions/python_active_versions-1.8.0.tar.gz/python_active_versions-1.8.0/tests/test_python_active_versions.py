#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Tests for `python_active_versions` package."""

from unittest.mock import patch

from python_active_versions import __version__
from python_active_versions.cli_tools.cli import get_python_versions


def test_py_version():
    """Dummy test to print python version used by pytest."""
    import sys

    print(f"in TEST: {sys.version}  -- {sys.version_info}")
    # if sys.version_info <= (3, 9, 18):
    #     # 3.9 OK
    #     assert True
    # else:
    #     # 3.10 FAIL
    #     assert False


def test_help(runner):
    """Test tool --help.

    Arguments:
        runner: Click runner
    """
    result = runner.invoke(get_python_versions, ['--help'])
    assert result.exit_code == 0
    assert '--help' in result.output


def test_version(runner):
    """Test tool --version.

    Arguments:
        runner: Click runner
    """
    result = runner.invoke(get_python_versions, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output


@patch('requests_html.HTMLSession.get')
def test_api_calls(patched_get, runner):
    """Test API calls.

    Arguments:
        patched_get: patched get call
        runner: Click runner
    """
    _ = runner.invoke(get_python_versions, [])
    patched_get.assert_any_call("https://devguide.python.org/versions/")
    patched_get.assert_any_call("https://www.python.org/downloads/")
