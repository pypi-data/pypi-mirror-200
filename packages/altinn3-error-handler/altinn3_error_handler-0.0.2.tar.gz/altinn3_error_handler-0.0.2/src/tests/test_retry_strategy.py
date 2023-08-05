from typing import Any
from time import perf_counter
from unittest.mock import MagicMock, Mock

import pytest

from altinn3_error_handler.strategies.retry_strategy import RetryStrategy


VALUE_TOO_SMALL = "Value too small!"


# Direct unit tests
def test_ok():
    strategy = RetryStrategy()

    def func(n: int) -> int:
        return n % 5

    result = strategy.act(func, 8)

    assert result.invoke_result == 3
    assert result.exception is None


def test_simple_error():
    retries: int = 100
    count_mock = MagicMock()
    # to keep test short, backoff = 0 secs
    strategy = RetryStrategy(backoff=0, tries=retries, on_except_hook=count_mock.test)

    def func(n) -> int:
        return n % 5

    result = strategy.act(func, "bob")

    assert result.invoke_result is None
    assert isinstance(result.exception, TypeError)
    assert count_mock.test.call_count == retries


def test_unexpected_error_not_retried():
    retries: int = 100
    count_mock = MagicMock()
    # to keep test short, backoff = 0 secs
    strategy = RetryStrategy(handled_exceptions=(ZeroDivisionError,), backoff=0, tries=retries, on_except_hook=count_mock.test)

    def func(n) -> int:
        return n % 5

    result = None

    with pytest.raises(TypeError) as e:
        result = strategy.act(func, "bob")

    assert result is None
    assert str(e.value).startswith("not all arguments")
    assert count_mock.test.call_count == 0


def test_backoff():
    # 3 attempts with flat 1-second break inbetween - total 2 sec:
    # attempt -> 1-sec break -> attempt -> 1-sec break -> attempt -> error!
    min_time = 1.8  # Apply a small margin of error since precision of sleep() is OS-dependent
    call_mock = MagicMock()
    strategy = RetryStrategy(tries=3, backoff=1, backoff_exponent=1, on_except_hook=call_mock.test)

    def func(x) -> str:
        return str(f"Result was: '{x % 10}'")

    started_at = perf_counter()

    result = strategy.act(func, "test")

    stopped_at = perf_counter()

    assert (stopped_at - started_at) > min_time
    assert (stopped_at - started_at) < min_time + 1
    assert result.invoke_result is None
    assert call_mock.test.call_count == 3


def test_backoff_exponential():
    # 3 attempts with 2-second backoff and exponential backoff increase - total 6 sec:
    # attempt -> 2-sec break -> attempt -> 4-sec break -> attempt -> error!
    min_time = 5.80  # Apply a small margin of error since precision of sleep() is OS-dependent
    call_mock = MagicMock()
    strategy = RetryStrategy(tries=3, backoff=2, backoff_exponent=2, on_except_hook=call_mock.test)

    def func(x) -> str:
        return str(f"Result was: '{x % 10}'")

    started_at = perf_counter()

    result = strategy.act(func, "test")

    stopped_at = perf_counter()

    assert (stopped_at - started_at) > min_time
    assert (stopped_at - started_at) < min_time + 1
    assert result.invoke_result is None
    assert call_mock.test.call_count == 3


def test_retries_on_alternate_connectio():
    count_mock = MagicMock()

    def alt_check(f_result: str, expected: str, counter: Any):
        if f_result != expected:
            counter.count()
            raise ValueError("Returned value doesn't meet expectations!")

    def func(x: int) -> str:
        return f"Result: {x * 2}"

    strategy = RetryStrategy(tries=3, backoff=0, alternate_error_check=alt_check, alternate_error_check_args={"expected": "Ok!", "counter": count_mock})

    result = strategy.act(func, 2)

    assert result.invoke_result is None
    assert count_mock.count.call_count == 3
    assert isinstance(result.exception, ValueError)


def test_retries_on_alternate_condition_ok():
    count_mock = MagicMock()

    def alt_check(f_result: str, expected: str, counter: Any):
        if f_result != expected:
            counter.count()
            raise ValueError("Returned value doesn't meet expectations!")

    def func(x: int) -> str:
        return f"Result: {x * 2}"

    strategy = RetryStrategy(tries=3, backoff=0, alternate_error_check=alt_check, alternate_error_check_args={"expected": "Result: 4", "counter": count_mock})

    result = strategy.act(func, 2)

    assert result.invoke_result == "Result: 4"
    assert count_mock.count.call_count == 0
    assert result.exception is None


def test_retries_fail_first_call():
    retries: int = 100

    return_different_func = [i for i in range(retries)]

    count_mock = MagicMock()
    fail_mock = Mock()
    fail_mock.my_func.side_effect = return_different_func

    # to keep test short, backoff = 0 secs
    strategy = RetryStrategy(backoff=0, tries=retries, on_except_hook=count_mock.test)

    def func(n, fake_service) -> int:
        val = fake_service.my_func()
        if val < n:
            raise ValueError(VALUE_TOO_SMALL)
        return val

    result = strategy.act(func, 1, fail_mock)

    assert count_mock.test.call_count == 1
    assert result.invoke_result == 1
    assert result.exception is None


def test_retries_fail_multiple_calls():
    retries: int = 100

    return_different_func = [i for i in range(retries)]

    count_mock = MagicMock()
    fail_mock = Mock()
    fail_mock.my_func.side_effect = return_different_func

    # to keep test short, backoff = 0 secs
    strategy = RetryStrategy(backoff=0, tries=retries, on_except_hook=count_mock.test)

    def func(n, fake_service) -> int:
        val = fake_service.my_func()
        if val < n:
            raise ValueError(VALUE_TOO_SMALL)
        return val

    result = strategy.act(func, 50, fail_mock)

    assert count_mock.test.call_count == 50
    assert result.invoke_result == 50
    assert result.exception is None


def test_retries_alternate_fail_first_call():
    retries: int = 100

    return_different_func = [i for i in range(retries)]

    def alt_check(res: str, limit: int):
        if int(res) < limit:
            raise ValueError("Alt Check: Value too small!")

    count_mock = MagicMock()
    fail_mock = Mock()
    fail_mock.my_func.side_effect = return_different_func

    # to keep test short, backoff = 0 secs
    strategy = RetryStrategy(backoff=0, tries=retries, on_except_hook=count_mock.test, alternate_error_check=alt_check, alternate_error_check_args={"limit": 1})

    def func(fake_service) -> int:
        val = fake_service.my_func()
        return val

    result = strategy.act(func, fail_mock)

    assert count_mock.test.call_count == 1
    assert result.invoke_result == 1
    assert result.exception is None


def test_retries_alternate_fail_multiple_calls():
    retries: int = 100

    return_different_func = [i for i in range(retries)]

    def alt_check(res: str, limit: int):
        if int(res) < limit:
            raise ValueError("Alt Check: Value too small!")

    count_mock = MagicMock()
    fail_mock = Mock()
    fail_mock.my_func.side_effect = return_different_func

    # to keep test short, backoff = 0 secs
    strategy = RetryStrategy(
        backoff=0,
        tries=retries,
        on_except_hook=count_mock.test,
        alternate_error_check=alt_check,
        alternate_error_check_args={"limit": 50}
    )

    def func(n, fake_service) -> int:
        val = fake_service.my_func()
        if val < n:
            raise ValueError(VALUE_TOO_SMALL)
        return val

    result = strategy.act(func, 0, fail_mock)

    assert count_mock.test.call_count == 50
    assert fail_mock.my_func.call_count == 51
    assert result.invoke_result == 50
    assert result.exception is None
