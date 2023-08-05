from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_in(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 not in assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_not_in(assert_object1, assert_object2, when_failure_print_message: str):
    if assert_object1 in assert_object2:
        assert_fail_message(when_failure_print_message)


def assert_length_equal(assert_object1, assert_object2, when_failure_print_message: str):
    if len(assert_object1) != len(assert_object2):
        assert_fail_message(when_failure_print_message)


def assert_length_not_equal(assert_object1, assert_object2, when_failure_print_message: str):
    if len(assert_object1) == len(assert_object2):
        assert_fail_message(when_failure_print_message)


def assert_sort_list_equal(assert_list1: list, assert_list2: list, when_failure_print_message: str):
    if assert_list1.sort() != assert_list2.sort():
        assert_fail_message(when_failure_print_message)


def assert_sort_list_not_equal(assert_list1: list, assert_list2: list, when_failure_print_message: str):
    if assert_list1.sort() == assert_list2.sort():
        assert_fail_message(when_failure_print_message)
