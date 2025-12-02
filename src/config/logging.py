import logging
import logging.config
import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": sys.stdout
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
}


def configure_logging(level: str = "INFO"):
    """Configure logging for the application.

    Note: The JSON formatter requires the `python-json-logger` package if you want
    to enable JSON formatting. The default is a human-readable formatter.
    """
    # Apply base config
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger().setLevel(level)
