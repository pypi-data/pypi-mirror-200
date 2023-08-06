# SPDX-FileCopyrightText: 2022 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Test utils module."""

import logging
from unittest.mock import patch

from python_active_versions.utility import configure_logger


@patch('logging.basicConfig')
def test_logger(patched_log):
    """Testing configure_logger.

    Arguments:
        patched_log: patched basicConfig method
    """
    configure_logger()
    patched_log.assert_called_with(
        level=logging.INFO, format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s', handlers=None
    )

    configure_logger('info')
    patched_log.assert_called_with(
        level=logging.INFO, format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s', handlers=None
    )

    configure_logger('debug')
    patched_log.assert_called_with(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s',
        handlers=None,
    )

    configure_logger('warning')
    patched_log.assert_called_with(
        level=logging.WARN, format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s', handlers=None
    )

    configure_logger('error')
    patched_log.assert_called_with(
        level=logging.ERROR,
        format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s',
        handlers=None,
    )
