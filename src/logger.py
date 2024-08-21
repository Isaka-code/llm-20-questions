"""logger.py"""

import logging
from typing import Any
from logging import getLogger, Formatter, FileHandler, StreamHandler, DEBUG


class MockLogger:
    def __init__(self, exp_version: str) -> None:
        pass

    def log(self, *args: Any, level: str = "info", is_print: bool = False) -> None:
        pass


class Logger:
    def __init__(self, exp_version: str) -> None:
        log_file = f"{exp_version}.log"
        self.logger = getLogger(exp_version)
        self.logger.setLevel(DEBUG)
        formatter = Formatter("[%(levelname)s] %(asctime)s >>\n%(message)s")

        file_handler = FileHandler(log_file)
        file_handler.setLevel(DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = StreamHandler()
        stream_handler.setLevel(DEBUG)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def _log(self, message: Any, level: str, is_print: bool) -> None:
        log_function = {
            "debug": self.logger.debug,
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical,
        }.get(level.lower(), self.logger.info)

        log_function(message)

        if is_print:
            print(message)

    def log(self, *args: Any, level: str = "info", is_print: bool = False) -> None:
        for arg in args:
            self._log(arg, level, is_print)


if __name__ == "__main__":
    logger = Logger("exp_000")
    logger.log("test message", level="info")
    logger.log("no print", level="info", is_print=False)
    logger.log("debug message", level="debug")
    logger.log("warning message", level="warning")
    logger.log("error message", level="error")
    logger.log("critical message", level="critical")
