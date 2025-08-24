import logging
import asyncio


class IgnoreCancelledFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.exc_info:
            return not isinstance(record.exc_info[1], asyncio.CancelledError)
        return "CancelledError" not in record.getMessage()


def uvicorn_log_config(dev: bool = True) -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "ignore_cancelled": {
                "()": "z8ter.logging_utils.IgnoreCancelledFilter"
            }
        },
        "formatters": {
            "plain": {"format": "%(message)s"}
        },
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
            "uvicorn":        {"handlers": ["rich"], "level": "INFO",
                               "propagate": False},
            "uvicorn.error":  {"handlers": ["rich"], "level": "INFO",
                               "propagate": False},
            "uvicorn.access": {"handlers": ["rich"],
                               "level": "WARNING" if dev else "INFO",
                               "propagate": False},
            "uvicorn.lifespan": {"handlers": ["rich"],
                                 "level": "INFO", "propagate": False},
            "z8ter":         {"handlers": ["rich"],
                              "level": "DEBUG" if dev else "INFO",
                              "propagate": False},
        },
        "root": {"handlers": ["rich"], "level": "DEBUG" if dev else "INFO"},
    }
