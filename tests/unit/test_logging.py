"""Unit tests for centralized logging."""

import logging

from src.utilities.logging import get_logger


def cleanup_logger(logger):
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


def test_logger_configuration():
    logger = get_logger("aerovision.test.configuration")

    try:
        assert logger.name == "aerovision.test.configuration"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
    finally:
        cleanup_logger(logger)


def test_repeated_configuration_does_not_duplicate_handlers():
    logger = get_logger("aerovision.test.duplicates")

    try:
        get_logger("aerovision.test.duplicates")

        assert len(logger.handlers) == 1
    finally:
        cleanup_logger(logger)


def test_file_logging_writes_message(tmp_path):
    log_path = tmp_path / "logs" / "pipeline.log"
    logger = get_logger(
        "aerovision.test.file",
        log_file=log_path,
    )

    try:
        logger.info("AEROVISION pipeline test message")

        for handler in logger.handlers:
            handler.flush()

        content = log_path.read_text(encoding="utf-8")
        assert "AEROVISION pipeline test message" in content
        assert "INFO" in content
    finally:
        cleanup_logger(logger)
