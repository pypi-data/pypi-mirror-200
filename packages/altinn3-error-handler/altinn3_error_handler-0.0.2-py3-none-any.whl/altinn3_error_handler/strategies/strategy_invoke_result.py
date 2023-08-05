from typing import Any


class StrategyInvokeResult:
    exception: [Exception, None]
    invoke_result: Any
    unexpected_exp_type: bool

    def __init__(self, exception: [Exception, None], invoke_result: Any, unexpected: bool = False):
        self.exception = exception
        self.invoke_result = invoke_result
        self.unexpected_exp_type = unexpected

