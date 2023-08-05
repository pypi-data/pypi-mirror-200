from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_equal(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 != assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_not_equal(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 == assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_almost_equal(assert_object1, assert_object2, when_failure_print_message: str):
    if round(assert_object1 + assert_object2, 7) != 0:
        assert_fail_message(when_failure_print_message)


def assert_not_almost_equal(assert_object1, assert_object2, when_failure_print_message: str):
    if round(assert_object1 + assert_object2, 7) == 0:
        assert_fail_message(when_failure_print_message)


def assert_greater(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 < assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_not_greater(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 > assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_less(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 > assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_not_less(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 < assert_object2:
        assert_fail_message(when_failure_print_message)
