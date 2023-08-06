"""Форматирование вывода в консоль."""

# pyright: reportUnnecessaryComparison=false

import logging

from .const import CHAR_IN_LINE, FORMAT


class StreamFormatter(logging.Formatter):
    """Custom formatter for console output."""

    color_green: str = "\x1b[32;20m"
    color_grey: str = "\x1b[38;20m"
    color_yellow: str = "\x1b[33;20m"
    color_red: str = "\x1b[31;20m"
    color_bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"

    def get_format(self: "StreamFormatter", text: str, levelno: int) -> str:
        """Цвет сообщения.

        :param text: текст, цвет которого нужно изменить
        :param levelno: класс сообщения
        :return: текст с измененным текстом
        """
        out_text: str = ""
        match levelno:
            case logging.DEBUG:
                out_text = self.color_grey + text + self.reset
            case logging.INFO:
                out_text = self.color_green + text + self.reset
            case logging.WARNING:
                out_text = self.color_yellow + text + self.reset
            case logging.ERROR:
                out_text = self.color_red + text + self.reset
            case logging.CRITICAL:
                out_text = self.color_bold_red + text + self.reset
            case _:
                out_text = text
        return out_text

    def format(self: "StreamFormatter", record: logging.LogRecord) -> str:
        """Format function.

        :param record: запись логгера
        :return: отформатированная запись логгера
        """
        log_fmt = self.get_format(FORMAT, record.levelno)
        formatter = logging.Formatter(log_fmt)
        return (
            formatter.format(record)
            + "\n"
            + self.get_format("-" * CHAR_IN_LINE, record.levelno)
        )
