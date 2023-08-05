import unittest.mock
from typing import Any

import pytest
from unittest.mock import MagicMock

from altinn3_error_handler.error_handler import error_handler


SHOULDNT_REACH = "Shouldn't reach this!"


def test_no_exception_ok():
    @error_handler
    def simple(a: int, b: int) -> int:
        return int(a / b)

    result = simple(6, 2)

    assert result == 3


def test_exception_raises():
    @error_handler
    def simple(a: int, b: int) -> int:
        return int(a / b)

    # noinspection PyUnusedLocal
    result: Any = None

    with pytest.raises(ZeroDivisionError):
        result = simple(2, 0)
        raise AssertionError(SHOULDNT_REACH)

    assert result is None


def test_exception_supress():
    @error_handler(re_raise=False)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    result = simple(2, 0)

    assert result is None


def test_ok_custom_logger():
    logger_mock = MagicMock()

    @error_handler(logger=logger_mock)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    result = simple(4, 2)

    assert result == 2
    logger_mock.error.assert_not_called()


def test_exception_custom_logger():
    logger_mock = MagicMock()

    @error_handler(logger=logger_mock)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    # noinspection PyUnusedLocal
    result: Any = None

    with pytest.raises(ZeroDivisionError):
        result = simple(2, 0)
        raise AssertionError(SHOULDNT_REACH)

    assert result is None
    logger_mock.error.assert_called_once()


def test_exception_nested_custom_logger():
    logger_mock = MagicMock()
    logger_mock2 = MagicMock()

    @error_handler(logger=logger_mock2)
    @error_handler(logger=logger_mock)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    # noinspection PyUnusedLocal
    result: Any = None

    with pytest.raises(ZeroDivisionError):
        result = simple(2, 0)
        raise AssertionError(SHOULDNT_REACH)

    assert result is None
    logger_mock.error.assert_called_once()
    logger_mock2.error.assert_called_once()


def test_ok_exception_callback():
    callback_mock = MagicMock()

    @error_handler(post_exception_hook=callback_mock)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    result = simple(4, 2)

    assert result == 2
    callback_mock.error.assert_not_called()


def test_exception_exception_callback():
    callback_mock = MagicMock()

    @error_handler(post_exception_hook=callback_mock)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    # noinspection PyUnusedLocal
    result: Any = None

    with pytest.raises(ZeroDivisionError):
        result = simple(2, 0)
        raise AssertionError(SHOULDNT_REACH)

    assert result is None
    callback_mock.assert_called_once()


def test_exception_exception_callback_with_args():
    callback_mock = MagicMock()

    cb_kwargs = {"arg1": 123, "foo": "bar", "dilbert": "dogbert"}

    @error_handler(post_exception_hook=callback_mock, post_exp_hook_kwargs=cb_kwargs)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    # noinspection PyUnusedLocal
    result: Any = None

    with pytest.raises(ZeroDivisionError):
        result = simple(2, 0)
        raise AssertionError(SHOULDNT_REACH)

    assert result is None
    callback_mock.assert_called_once_with(unittest.mock.ANY, **cb_kwargs)


def test_supress_exception_exception_callback_with_args():
    callback_mock = MagicMock()

    cb_kwargs = {"arg1": 123, "foo": "bar", "dilbert": "dogbert"}

    @error_handler(re_raise=False, post_exception_hook=callback_mock, post_exp_hook_kwargs=cb_kwargs)
    def simple(a: int, b: int) -> int:
        return int(a / b)

    result = simple(2, 0)

    assert result is None
    callback_mock.assert_called_once_with(unittest.mock.ANY, **cb_kwargs)
