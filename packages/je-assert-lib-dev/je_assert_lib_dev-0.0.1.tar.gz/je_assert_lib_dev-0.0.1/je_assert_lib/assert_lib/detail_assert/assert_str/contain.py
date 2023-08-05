from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_str_contain(string_object: str, contain_str: str, when_failure_print_message: str):
    if contain_str not in string_object:
        assert_fail_message(when_failure_print_message)


def assert_str_contains(string_object: str, contain_str_list: str, when_failure_print_message: str):
    for contain_str in contain_str_list:
        if contain_str not in string_object:
            assert_fail_message(when_failure_print_message)


def assert_str_not_contain(string_object: str, contain_str: str, when_failure_print_message: str):
    if contain_str in string_object:
        assert_fail_message(when_failure_print_message)


def assert_str_not_contains(string_object: str, contain_str_list: str, when_failure_print_message: str):
    for contain_str in contain_str_list:
        if contain_str in string_object:
            assert_fail_message(when_failure_print_message)
