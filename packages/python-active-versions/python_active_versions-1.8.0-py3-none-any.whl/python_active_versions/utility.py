# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Module with utility methods."""

import logging


def configure_logger(level: str = 'info') -> None:
    """Configure logger facility from server or client in same way, changing only the output file.

    Arguments:
        level: level of logging facility
    """
    # configure logging
    _log_level = logging.INFO
    if level.lower() == 'debug':
        _log_level = logging.DEBUG
    elif level.lower() == 'warning':
        _log_level = logging.WARNING
    elif level.lower() == 'error':
        _log_level = logging.ERROR

    logging.basicConfig(
        level=_log_level,
        format='%(asctime)s [%(levelname)s - %(filename)s:%(lineno)d]    %(message)s',
        handlers=None,
    )
