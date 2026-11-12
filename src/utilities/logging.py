"""Centralized logging utilities for AEROVISION 360."""

import logging
from pathlib import Path

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: str | Path | None = None,
) -> logging.Logger:
    """Return a consistently configured logger without duplicate handlers."""
    if not name or not name.strip():
        raise ValueError("Logger name cannot be empty.")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    def add_handler(handler: logging.Handler, key: str) -> None:
        existing = any(
            getattr(item, "_aerovision_handler_key", None) == key
            for item in logger.handlers
        )
        if not existing:
            handler.setFormatter(formatter)
            handler._aerovision_handler_key = key
            logger.addHandler(handler)
        else:
            handler.close()

    add_handler(logging.StreamHandler(), "console")

    if log_file is not None:
        target = Path(log_file).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        add_handler(
            logging.FileHandler(target, encoding="utf-8"),
            f"file:{target}",
        )

    return logger
