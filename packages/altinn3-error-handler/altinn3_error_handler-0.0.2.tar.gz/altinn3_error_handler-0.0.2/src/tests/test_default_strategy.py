from typing import Any
import pytest
from unittest.mock import MagicMock
from altinn3_error_handler.error_handler import error_handler
from altinn3_error_handler.strategies.default_handling_strategy import DefaultHandlingStrategy

SHOULDNT_REACH = "Shouldn't reach this!"
UNEXPECTED = "Unexpected result!"


def alt_check(n: int):
    if n < 0:
        raise ValueError(UNEXPECTED)


def alt_check_args(n: int, target: int):
    if n != target:
        raise ValueError(UNEXPECTED)


# Direct unit tests
def test_no_error():
    strategy = DefaultHandlingStrategy()

    def func() -> str:
        print("Hello!")
        return "Ok"

    result = strategy.act(func)

    assert result.invoke_result == "Ok"
    assert result.exception is None
    assert not result.unexpected_exp_type


def test_expected_error():
    strategy = DefaultHandlingStrategy(handled_exceptions=(TypeError,))

    def func(x: int) -> str:
        print(100 % x)
        return "Ok"

    result = strategy.act(func, "bob")

    assert result.invoke_result is None
    assert isinstance(result.exception, TypeError)
    assert result.unexpected_exp_type == False


def test_unexpected_error():
    strategy = DefaultHandlingStrategy(handled_exceptions=(ValueError,))

    def func(x: int) -> str:
        print(100 % x)
        return "Ok"

    # noinspection PyUnusedLocal
    result: Any = None

    with pytest.raises(TypeError):
        result = strategy.act(func, 432)
        result = strategy.act(func, result)
        raise AssertionError(SHOULDNT_REACH)

    assert result.invoke_result == "Ok"


def test_alternate_error_check_ok():
    strategy = DefaultHandlingStrategy(alternate_error_check=alt_check)

    def func(n: int) -> int:
        return n - 5

    result = strategy.act(func, 10)

    assert result.invoke_result == 5


def test_alternate_error_check_error():
    strategy = DefaultHandlingStrategy(alternate_error_check=alt_check)

    def func(n: int) -> int:
        return n - 5

    result = strategy.act(func, 3)

    assert result.invoke_result is None
    assert isinstance(result.exception, ValueError)
    assert str(result.exception) == UNEXPECTED


def test_alternate_error_with_args_check_ok():
    strategy = DefaultHandlingStrategy(alternate_error_check=alt_check_args, alternate_error_check_args={"target": 5})

    def func(n: int) -> int:
        return n - 5

    result = strategy.act(func, 10)

    assert result.invoke_result == 5


def test_alternate_error_check_with_args_error():
    strategy = DefaultHandlingStrategy(alternate_error_check=alt_check_args, alternate_error_check_args={"target": 5})

    def func(n: int) -> int:
        return n - 5

    result = strategy.act(func, 3)

    assert result.invoke_result is None
    assert isinstance(result.exception, ValueError)
    assert str(result.exception) == UNEXPECTED


# Tests using through handler
def test_handler_with_exception_list_ok():
    strategy = DefaultHandlingStrategy(handled_exceptions=(TypeError,))

    @error_handler(strategy=strategy)
    def func(x) -> str:
        print(100 % x)
        return "Ok"

    result = func(432)

    assert result == "Ok"


def test_handler_with_exception_list_error():
    check_mock = MagicMock()

    strategy = DefaultHandlingStrategy(handled_exceptions=(TypeError,), on_except_hook=check_mock.test)

    @error_handler(strategy=strategy)
    def func(x) -> str:
        print(100 % x)
        return "Ok"

    # noinspection PyUnusedLocal
    result = ""

    with pytest.raises(TypeError):
        result = func("Bob")
        raise AssertionError(SHOULDNT_REACH)

    assert result == ""
    check_mock.test.assert_called_once()


def test_handler_with_exception_list_unexpected_error():
    check_mock = MagicMock()

    strategy = DefaultHandlingStrategy(handled_exceptions=(ValueError,), on_except_hook=check_mock.test)

    @error_handler(strategy=strategy)
    def func(x) -> str:
        print(100 % x)
        return "Ok"

    # noinspection PyUnusedLocal
    result = ""

    with pytest.raises(TypeError):
        result = func("Bob")
        raise AssertionError(SHOULDNT_REACH)

    assert result == ""
    check_mock.test.assert_not_called()
