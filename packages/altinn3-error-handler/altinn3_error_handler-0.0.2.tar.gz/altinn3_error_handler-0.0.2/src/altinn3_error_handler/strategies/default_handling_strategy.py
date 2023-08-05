from typing import Any, Callable, Dict, Tuple, Type

from altinn3_error_handler.strategies.error_handling_strategy import ErrorHandlingStrategy
from altinn3_error_handler.strategies.strategy_invoke_result import StrategyInvokeResult


class DefaultHandlingStrategy(ErrorHandlingStrategy):

    def __init__(
            self,
            *,
            handled_exceptions: Tuple[Type[Exception], ...] = None,
            on_except_hook: Callable = None,
            on_except_hook_args: Dict[str, Any] = None,
            alternate_error_check: Callable = None,
            alternate_error_check_args: Dict[str, Any] = None
    ):
        super().__init__(
            handled_exceptions=handled_exceptions,
            on_except_hook=on_except_hook,
            on_except_hook_args=on_except_hook_args,
            alternate_error_check=alternate_error_check,
            alternate_error_check_args=alternate_error_check_args
        )

    def act(self, func: Callable, *args, **kwargs) -> StrategyInvokeResult:
        try:
            result = func(*args, **kwargs)
            if self.alternate_error_check is not None:
                self.alternate_error_check(result, **self.alternate_error_check_args)
            return StrategyInvokeResult(exception=None, invoke_result=result)
        except self.handled_exceptions as e:
            self.logger.error(f"An exception was encountered during execution of {func.__name__}: {e}", exc_info=e)
            if self.on_except_hook is not None:
                self.on_except_hook(e, **self.on_except_hook_args)
            return StrategyInvokeResult(exception=e, invoke_result=None)
        except Exception as e:
            self.logger.error(f"Unexpected exception encountered during execution of {func.__name__}: {e}", exc_info=e)
            raise e
