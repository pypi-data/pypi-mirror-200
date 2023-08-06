"""Настройка логгирования.

В точке входа в программу:

from shared import Logger
Logger()

В файлах:

import logging
log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)
"""

import logging
import os
import socket
from logging.handlers import RotatingFileHandler
from typing import Iterable

from .const import FORMAT, LOG_SIZE
from .file_formatter import FileFormatter
from .stream_formatter import StreamFormatter


class Logger(object):
    """Логгер."""

    def __init__(
        self,
        folder_name: str = "logs",
        file_name: str = "log",
        output_to_console: bool = False,
    ) -> None:
        """Логгер.

        Parameters
        ----------
        folder_name: str
            папка для сохранения текстовых логов
        file_name: str
            название файла логов
        output_to_console: bool
            True - выводить сообщения в консоль
        """
        self.__create_folder(folder_name)
        handlers: list[logging.Handler] = []
        handlers.append(self.__create_file_handler(folder_name, file_name))
        if output_to_console:
            handlers.append(self.__create_stream_handler())
        self.__logging_config(handlers)
        self.__post_init_message(output_to_console)

    def __create_folder(self, folder_name: str):
        os.makedirs(folder_name, exist_ok=True)

    def __create_file_handler(
        self,
        folder_name: str,
        file_name: str,
    ) -> logging.Handler:
        file_handler: logging.Handler = RotatingFileHandler(
            filename="{folder_name}/{file_name}.log".format(
                folder_name=folder_name,
                file_name=file_name,
            ),
            mode="a",
            maxBytes=LOG_SIZE,
            backupCount=2,
            encoding=None,
            delay=False,
        )
        file_handler.setFormatter(FileFormatter())
        return file_handler

    def __create_stream_handler(self) -> logging.Handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(StreamFormatter())
        return stream_handler

    def __logging_config(self, handlers: Iterable[logging.Handler]) -> None:
        logging.basicConfig(
            format=FORMAT,
            level=logging.INFO,
            handlers=handlers,
        )

    def __post_init_message(self, output_to_console: bool):
        log = logging.getLogger(__name__)
        log.info("Start at host: {0}".format(socket.gethostname()))
        if output_to_console:
            log.warning("Активирован вывод сообщений в консоль")
