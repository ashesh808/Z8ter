"""Logging utilities for Z8ter.

This module provides:
- A filter (`IgnoreCancelledFilter`) to silence noisy asyncio
  `CancelledError` logs.
- A preconfigured logging dict for Uvicorn (`uvicorn_log_config`)
  using Rich for nicer console output.

Usage:
    import logging.config
    from z8ter.logging_utils import uvicorn_log_config

    logging.config.dictConfig(uvicorn_log_config(dev=True))
"""

import asyncio
import logging


class IgnoreCancelledFilter(logging.Filter):
    """Filter out asyncio.CancelledError log records.

    Prevents cancelled tasks (a normal ASGI/Uvicorn occurrence)
    from cluttering the log output.

    Behavior:
        - If record.exc_info contains a CancelledError, suppress it.
        - Otherwise, filter out if the message text includes
          "CancelledError".
    """


def filter(self, record: logging.LogRecord) -> bool:
    """Decide whether a log record should be emitted."""
    if record.exc_info:
        return not isinstance(record.exc_info[1], asyncio.CancelledError)
    return "CancelledError" not in record.getMessage()


def uvicorn_log_config(dev: bool = True) -> dict:
    """Return a logging configuration dict for Uvicorn.

    Args:
        dev: If True, enable more verbose/debug-friendly settings.
            - Sets log level to DEBUG for app + root.
            - Lowers uvicorn.access to WARNING (suppress noisy access logs).
        If False (prod):
            - Sets log level to INFO.
            - Leaves access logs enabled at INFO.

    Returns:
        dict: A standard logging configuration compatible with
        `logging.config.dictConfig`.

    Notes:
        - Uses RichHandler for colorful, structured console output.
        - Attaches IgnoreCancelledFilter to silence cancelled tasks.

    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "ignore_cancelled": {"()": "z8ter.logging_utils.IgnoreCancelledFilter"}
        },
        "formatters": {"plain": {"format": "%(message)s"}},
        "handlers": {
            "rich": {
                "class": "rich.logging.RichHandler",
                "rich_tracebacks": True,
                "markup": True,
                "show_level": True,
                "show_time": True,
                "show_path": False,
                "log_time_format": "[%X]",
                "level": "DEBUG" if dev else "INFO",
                "formatter": "plain",
                "filters": ["ignore_cancelled"],
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["rich"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["rich"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["rich"],
                "level": "WARNING" if dev else "INFO",
                "propagate": False,
            },
            "uvicorn.lifespan": {
                "handlers": ["rich"],
                "level": "INFO",
                "propagate": False,
            },
            "z8ter": {
                "handlers": ["rich"],
                "level": "DEBUG" if dev else "INFO",
                "propagate": False,
            },
        },
        "root": {"handlers": ["rich"], "level": "DEBUG" if dev else "INFO"},
    }
