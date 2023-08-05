from logging import Logger, getLogger
from typing import Any, Callable, Dict, Tuple, Type

from altinn3_error_handler.strategies.strategy_invoke_result import StrategyInvokeResult


class ErrorHandlingStrategy:
    handled_exceptions: Tuple[Type[Exception], ...]
    on_except_hook: Callable
    on_except_hook_args: Dict[str, Any]
    alternate_error_check: Callable
    alternate_error_check_args: Dict[str, Any]
    logger: Logger

    def __init__(
            self,
            *,
            handled_exceptions: Tuple[Type[Exception]] = None,
            on_except_hook: Callable = None,
            on_except_hook_args: Dict[str, Any] = None,
            alternate_error_check: Callable = None,
            alternate_error_check_args: Dict[str, Any] = None
    ):
        self.handled_exceptions = handled_exceptions
        self.on_except_hook = on_except_hook
        self.on_except_hook_args = on_except_hook_args
        self.alternate_error_check = alternate_error_check
        self.alternate_error_check_args = alternate_error_check_args
        self.logger = getLogger()

        if self.handled_exceptions is None:
            self.handled_exceptions = (Exception,)

        if self.on_except_hook_args is None:
            self.on_except_hook_args = {}

        if self.alternate_error_check_args is None:
            self.alternate_error_check_args = {}

    def act(self, func: Callable, *args, **kwargs) -> StrategyInvokeResult:
        """
        Override this function in the strategy implementations.
        Invokes and handles result of the function for which the strategy is applied
        :param func: Function for error handling
        :param args: function args
        :param kwargs: function kwargs
        :return: result of the invocation or eventual errors
        """
        pass

    def set_logger(self, logger: Logger):
        self.logger = logger
