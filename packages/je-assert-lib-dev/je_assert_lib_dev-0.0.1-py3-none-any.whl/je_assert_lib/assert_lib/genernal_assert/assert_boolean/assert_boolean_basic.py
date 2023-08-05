from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_true(assert_object1, when_failure_print_message: str):
    if (bool(assert_object1)) is False:
        assert_fail_message(when_failure_print_message)


def assert_false(assert_object1, assert_object2, when_failure_print_message: str):
    if (bool(assert_object1)) is True:
        assert_fail_message(when_failure_print_message)


def assert_is(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 is not assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_is_not(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 is assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_is_none(assert_object1, when_failure_print_message: str):
    if assert_object1 is not None:
        assert_fail_message(when_failure_print_message)


def assert_is_not_none(assert_object1, when_failure_print_message: str):
    if assert_object1 is None:
        assert_fail_message(when_failure_print_message)
