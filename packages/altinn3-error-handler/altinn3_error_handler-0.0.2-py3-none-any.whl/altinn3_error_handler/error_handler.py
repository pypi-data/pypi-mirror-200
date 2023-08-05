import functools
import logging
from typing import Callable, Any, Dict

from altinn3_error_handler.strategies.error_handling_strategy import ErrorHandlingStrategy
from altinn3_error_handler.strategies.default_handling_strategy import DefaultHandlingStrategy
from altinn3_error_handler.strategies.strategy_invoke_result import StrategyInvokeResult


def error_handler(
        decorated_func=None,
        *,
        strategy: ErrorHandlingStrategy = None,
        logger: logging.Logger = None,
        re_raise: bool = True,
        post_exception_hook: Callable = None,
        post_exp_hook_kwargs: Dict[str, Any] = None
    ):
    if strategy is None:
        strategy = DefaultHandlingStrategy(on_except_hook=(lambda e: print(f"Exception: {e}")))
    if post_exp_hook_kwargs is None:
        post_exp_hook_kwargs = {}
    if logger is None:
        logger = logging.getLogger()
    strategy.set_logger(logger)

    def func_wrapper(func):
        @functools.wraps(func)
        def inner_handler(*args, **kwargs):
            result: StrategyInvokeResult = strategy.act(func, *args, *kwargs)
            if result.exception is not None:
                if post_exception_hook is not None:
                    post_exception_hook(result.exception, **post_exp_hook_kwargs)
                if re_raise:
                    raise result.exception
            return result.invoke_result
        return inner_handler
    return func_wrapper(decorated_func) if callable(decorated_func) else func_wrapper
    