from sys import stderr


def assert_is_list(assert_object, when_failure_print_message: str):
    if type(assert_object) is not list:
        assert_fail_message(when_failure_print_message)


def assert_is_not_list(assert_object, when_failure_print_message: str):
    if type(assert_object) is list:
        assert_fail_message(when_failure_print_message)


def assert_is_tuple(assert_object, when_failure_print_message: str):
    if type(assert_object) is not tuple:
        assert_fail_message(when_failure_print_message)


def assert_is_not_tuple(assert_object, when_failure_print_message: str):
    if type(assert_object) is tuple:
        assert_fail_message(when_failure_print_message)


def assert_is_range(assert_object, when_failure_print_message: str):
    if type(assert_object) is not range:
        assert_fail_message(when_failure_print_message)


def assert_is_not_range(assert_object, when_failure_print_message: str):
    if type(assert_object) is range:
        assert_fail_message(when_failure_print_message)


def assert_is_set(assert_object, when_failure_print_message: str):
    if type(assert_object) is not set:
        assert_fail_message(when_failure_print_message)


def assert_is_not_set(assert_object, when_failure_print_message: str):
    if type(assert_object) is set:
        assert_fail_message(when_failure_print_message)


def assert_is_frozenset(assert_object, when_failure_print_message: str):
    if type(assert_object) is not frozenset:
        assert_fail_message(when_failure_print_message)


def assert_is_not_frozenset(assert_object, when_failure_print_message: str):
    if type(assert_object) is frozenset:
        assert_fail_message(when_failure_print_message)


def assert_is_dict(assert_object, when_failure_print_message: str):
    if type(assert_object) is not dict:
        assert_fail_message(when_failure_print_message)


def assert_is_not_dict(assert_object, when_failure_print_message: str):
    if type(assert_object) is dict:
        assert_fail_message(when_failure_print_message)
