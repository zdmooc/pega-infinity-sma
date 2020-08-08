import logging
from typing import Callable

from django.http import HttpRequest


class PismaLogger:
    """
    Custom logger class
    """

    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def _logger_decorator(logger: Callable):
        def wrapper(
            self,
            message: str,
            request: HttpRequest = None,
            user: str = None,
            *args,
            **kwargs
        ):
            if not user:
                if request:
                    user = request.user
                else:
                    user = "None"
            return logger(self, message, user=user, *args, **kwargs)

        return wrapper

    @_logger_decorator
    def debug(
        self,
        message: str,
        request: HttpRequest = None,
        user: str = None,
        *args,
        **kwargs
    ):
        self._logger.debug(message, extra={"user": user}, *args, **kwargs)

    @_logger_decorator
    def info(
        self,
        message: str,
        request: HttpRequest = None,
        user: str = None,
        *args,
        **kwargs
    ):
        self._logger.info(message, extra={"user": user}, *args, **kwargs)

    @_logger_decorator
    def warning(
        self,
        message: str,
        request: HttpRequest = None,
        user: str = None,
        *args,
        **kwargs
    ):
        self._logger.warning(message, extra={"user": user}, *args, **kwargs)

    @_logger_decorator
    def error(
        self,
        message: str,
        request: HttpRequest = None,
        user: str = None,
        *args,
        **kwargs
    ):
        self._logger.error(message, extra={"user": user}, *args, **kwargs)

    @_logger_decorator
    def critical(
        self,
        message: str,
        request: HttpRequest = None,
        user: str = None,
        *args,
        **kwargs
    ):
        self._logger.critical(message, extra={"user": user}, *args, **kwargs)
