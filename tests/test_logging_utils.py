from __future__ import annotations

import asyncio
import logging

from z8ter.logging_utils import filter as filter_record
from z8ter.logging_utils import uvicorn_log_config


def test_module_filter_function_detects_cancelled_errors() -> None:
    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=10,
        msg="task failed",
        args=(),
        exc_info=(None, asyncio.CancelledError(), None),
    )
    assert filter_record(None, record) is False

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=20,
        msg="CancelledError in message",
        args=(),
        exc_info=None,
    )
    assert filter_record(None, record) is False

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=30,
        msg="all good",
        args=(),
        exc_info=None,
    )
    assert filter_record(None, record) is True


def test_uvicorn_log_config_structure_changes_with_mode() -> None:
    dev_config = uvicorn_log_config(dev=True)
    prod_config = uvicorn_log_config(dev=False)

    rich_handler = dev_config["handlers"]["rich"]
    assert rich_handler["filters"] == ["ignore_cancelled"]
    assert rich_handler["level"] == "DEBUG"
    assert dev_config["loggers"]["z8ter"]["level"] == "DEBUG"

    assert prod_config["handlers"]["rich"]["level"] == "INFO"
    assert prod_config["loggers"]["z8ter"]["level"] == "INFO"
    assert prod_config["loggers"]["uvicorn.access"]["level"] == "INFO"
