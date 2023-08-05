from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_str_start_with(string_object: str, start_with: str, when_failure_print_message: str):
    if not string_object.startswith(start_with):
        assert_fail_message(when_failure_print_message)


def assert_str_not_start_with(string_object: str, start_with: str, when_failure_print_message: str):
    if string_object.startswith(start_with):
        assert_fail_message(when_failure_print_message)


def assert_str_end_with(string_object: str, end_with: str, when_failure_print_message: str):
    if not string_object.endswith(end_with):
        assert_fail_message(when_failure_print_message)


def assert_str_not_end_with(string_object: str, end_with: str, when_failure_print_message: str):
    if string_object.endswith(end_with):
        assert_fail_message(when_failure_print_message)
