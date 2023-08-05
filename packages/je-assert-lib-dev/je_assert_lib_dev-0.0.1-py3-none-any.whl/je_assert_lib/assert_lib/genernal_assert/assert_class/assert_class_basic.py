from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_is_instance(assert_object1, assert_object2, when_failure_print_message: str):
    if not isinstance(assert_object1, assert_object2):
        assert_fail_message(when_failure_print_message)


def assert_is_not_instance(assert_object1, assert_object2, when_failure_print_message: str):
    if isinstance(assert_object1, assert_object2):
        assert_fail_message(when_failure_print_message)


def assert_is_subclass(assert_object1, assert_object2, when_failure_print_message: str):
    if not issubclass(assert_object1, assert_object2):
        assert_fail_message(when_failure_print_message)


def assert_is_not_subclass(assert_object1, assert_object2, when_failure_print_message: str):
    if issubclass(assert_object1, assert_object2):
        assert_fail_message(when_failure_print_message)
