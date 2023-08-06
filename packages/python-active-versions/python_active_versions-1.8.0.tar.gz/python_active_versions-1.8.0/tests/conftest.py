# SPDX-FileCopyrightText: 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Pytest conftest."""

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="function")
def runner(request):
    """Pytest runner fixture.

    Arguments:
        request: pytest request

    Returns:
        Click CliRunner object
    """
    return CliRunner()
