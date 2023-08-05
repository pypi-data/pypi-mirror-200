import typing

from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_raise(
        function: typing.Callable,
        exception: Exception,
        when_failure_print_message: str,
        *args,
        **kwargs
):
    try:
        function(*args, **kwargs)
        assert_fail_message(when_failure_print_message)
    except exception:
        pass


def assert_no_raise(
        function: typing.Callable,
        exception: Exception,
        when_failure_print_message: str,
        *args,
        **kwargs
):
    try:
        function(*args, **kwargs)
    except exception:
        assert_fail_message(when_failure_print_message)
