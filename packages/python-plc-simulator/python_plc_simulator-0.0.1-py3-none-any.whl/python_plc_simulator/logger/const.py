"""Константы для логгеров."""

# flake8: noqa

from typing import Final

CHAR_IN_LINE: Final[int] = 80

FORMAT: Final[str] = (
    "%(levelname)s: %(asctime)s | "
    + "%(name)s:%(lineno)d - %(funcName)s | "
    + "\n-> %(message)s"
)

LOG_SIZE: Final[int] = 5 * 1024 * 1024
