"""test_logger.py"""

import pytest
from unittest.mock import patch, MagicMock
from logger import Logger


def test_logger_init():
    with patch("logger.FileHandler") as mock_file_handler, patch(
        "logger.StreamHandler"
    ) as mock_stream_handler:
        mock_file_handler.return_value = MagicMock()
        mock_stream_handler.return_value = MagicMock()

        logger = Logger("exp_test")

        mock_file_handler.assert_called_once_with("exp_test.log")
        mock_stream_handler.assert_called_once()


def test_logger_log_levels():
    with patch("logger.FileHandler"), patch("logger.StreamHandler"), patch(
        "logger.getLogger"
    ) as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger = Logger("exp_test")

        logger.log("info message", level="info")
        mock_logger.info.assert_called_once_with("info message")

        logger.log("debug message", level="debug")
        mock_logger.debug.assert_called_once_with("debug message")

        logger.log("warning message", level="warning")
        mock_logger.warning.assert_called_once_with("warning message")

        logger.log("error message", level="error")
        mock_logger.error.assert_called_once_with("error message")

        logger.log("critical message", level="critical")
        mock_logger.critical.assert_called_once_with("critical message")


if __name__ == "__main__":
    pytest.main()
