import requests
from typing import Any, Callable, Dict, Tuple, Type

from altinn3_error_handler.strategies.error_handling_strategy import ErrorHandlingStrategy
from altinn3_error_handler.strategies.retry_strategy import RetryStrategy
from altinn3_error_handler.strategies.strategy_invoke_result import StrategyInvokeResult


class HttpErrorStrategy(ErrorHandlingStrategy):
    retry_on_error: bool
    raise_on_4xx: bool
    raise_on_5xx: bool

    def __init__(
            self,
            handled_exceptions: Tuple[Type[Exception]] = None,
            on_except_hook: Callable = None,
            on_except_hook_args: Dict[str, Any] = None,
            retry_on_error: bool = False,
            raise_on_4xx: bool = False,
            raise_on_5xx: bool = False
    ):
        super().__init__(handled_exceptions=handled_exceptions, on_except_hook=on_except_hook, on_except_hook_args=on_except_hook_args)
        self.retry_on_error = retry_on_error
        self.raise_on_4xx = raise_on_4xx
        self.raise_on_5xx = raise_on_5xx

    def act(self, func: Callable, *args, **kwargs) -> StrategyInvokeResult:
        result: StrategyInvokeResult
        if self.retry_on_error:
            def validator(resp: requests.Response):
                if not isinstance(resp, requests.Response) or not str(resp.status_code).startswith("2"):
                    msg: str = f"Non-success status_code: {resp.status_code}" if hasattr(resp, "status_code") else "Unexpected response without status_code."
                    raise ValueError(msg)
            result = RetryStrategy(alternate_error_check=validator).act(func, *args, **kwargs)
            if result.exception is None:
                self._test_for_error(result.invoke_result)
            return result
        try:
            response = func(*args, **kwargs)
            self._test_for_error(response)
            return StrategyInvokeResult(exception=None, invoke_result=response)

        except self.handled_exceptions as e:
            self.logger.error(f"An exception was encountered during execution of {func.__name__}: {e}", e)
            if self.on_except_hook is not None:
                self.on_except_hook(e, **self.on_except_hook_args)
            return StrategyInvokeResult(exception=e, invoke_result=None)
        except Exception as e:
            self.logger.error(f"Unexpected exception encountered during execution of {func.__name__}: {e}", e)
            raise

    def _test_for_error(self, response: requests.Response):
        status_code: str = str(response.status_code)

        if status_code.startswith("2"):
            return

        if status_code.startswith("4") and self.raise_on_4xx:
            raise ValueError(f"Request returned an unexpected status code '{status_code}'\nContent: {response.text}")

        if status_code.startswith("5") and self.raise_on_5xx:
            raise ValueError(f"Request returned an unexpected status code '{status_code}'\nContent: {response.text}")