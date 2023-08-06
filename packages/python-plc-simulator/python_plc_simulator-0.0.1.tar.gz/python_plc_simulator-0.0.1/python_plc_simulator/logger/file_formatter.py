"""Форматтер для текстовых файлов."""

import logging

from .const import CHAR_IN_LINE, FORMAT


class FileFormatter(logging.Formatter):
    """Custom formatter for file output."""

    def format(self: "FileFormatter", record: logging.LogRecord) -> str:
        """Format function.

        :param record: запись логгера
        :return: отформатированная запись логгера
        """
        formatter = logging.Formatter(FORMAT)
        return "{0}\n{1}".format(formatter.format(record), "-" * CHAR_IN_LINE)
