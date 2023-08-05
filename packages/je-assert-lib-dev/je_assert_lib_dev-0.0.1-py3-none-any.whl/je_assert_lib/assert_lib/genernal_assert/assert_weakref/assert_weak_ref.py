from weakref import WeakMethod, WeakKeyDictionary, WeakValueDictionary, WeakSet

from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_is_weakmethod(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not WeakMethod:
        assert_fail_message(when_failure_print_message)


def assert_is_not_weakmethod(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is WeakMethod:
        assert_fail_message(when_failure_print_message)


def assert_is_weakkeydictionary(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not WeakKeyDictionary:
        assert_fail_message(when_failure_print_message)


def assert_is_not_weakkeydictionary(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is WeakKeyDictionary:
        assert_fail_message(when_failure_print_message)


def assert_is_weakvaluedictionary(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not WeakValueDictionary:
        assert_fail_message(when_failure_print_message)


def assert_is_not_weakvaluedictionary(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is WeakValueDictionary:
        assert_fail_message(when_failure_print_message)


def assert_is_weakset(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not WeakSet:
        assert_fail_message(when_failure_print_message)


def assert_is_not_weakset(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is WeakSet:
        assert_fail_message(when_failure_print_message)
