from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_str_empty(string_object: str, when_failure_print_message: str):
    if not string_object == "":
        assert_fail_message(when_failure_print_message)


def assert_str_not_empty(string_object: str, when_failure_print_message: str):
    if string_object == "":
        assert_fail_message(when_failure_print_message)


def assert_str_is_space(string_object: str, when_failure_print_message: str):
    if not string_object.isspace():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_space(string_object: str, when_failure_print_message: str):
    if string_object.isspace():
        assert_fail_message(when_failure_print_message)


def assert_str_is_title(string_object: str, when_failure_print_message: str):
    if not string_object.istitle():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_title(string_object: str, when_failure_print_message: str):
    if string_object.istitle():
        assert_fail_message(when_failure_print_message)


def assert_str_is_upper(string_object: str, when_failure_print_message: str):
    if not string_object.isupper():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_upper(string_object: str, when_failure_print_message: str):
    if string_object.isupper():
        assert_fail_message(when_failure_print_message)


def assert_str_is_numeric(string_object: str, when_failure_print_message: str):
    if not string_object.isnumeric():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_numeric(string_object: str, when_failure_print_message: str):
    if string_object.isnumeric():
        assert_fail_message(when_failure_print_message)


def assert_str_is_printable(string_object: str, when_failure_print_message: str):
    if not string_object.isprintable():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_printable(string_object: str, when_failure_print_message: str):
    if string_object.isprintable():
        assert_fail_message(when_failure_print_message)


def assert_str_is_lower(string_object: str, when_failure_print_message: str):
    if not string_object.islower():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_lower(string_object: str, when_failure_print_message: str):
    if string_object.islower():
        assert_fail_message(when_failure_print_message)


def assert_str_is_identifier(string_object: str, when_failure_print_message: str):
    if not string_object.isidentifier():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_identifier(string_object: str, when_failure_print_message: str):
    if string_object.isidentifier():
        assert_fail_message(when_failure_print_message)


def assert_str_is_digit(string_object: str, when_failure_print_message: str):
    if not string_object.isdigit():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_digit(string_object: str, when_failure_print_message: str):
    if string_object.isdigit():
        assert_fail_message(when_failure_print_message)


def assert_str_is_decimal(string_object: str, when_failure_print_message: str):
    if not string_object.isdecimal():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_decimal(string_object: str, when_failure_print_message: str):
    if string_object.isdecimal():
        assert_fail_message(when_failure_print_message)


def assert_str_is_ascii(string_object: str, when_failure_print_message: str):
    if not string_object.isascii():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_ascii(string_object: str, when_failure_print_message: str):
    if string_object.isascii():
        assert_fail_message(when_failure_print_message)


def assert_str_is_alpha(string_object: str, when_failure_print_message: str):
    if not string_object.isalpha():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_alpha(string_object: str, when_failure_print_message: str):
    if string_object.isalpha():
        assert_fail_message(when_failure_print_message)


def assert_str_is_alnum(string_object: str, when_failure_print_message: str):
    if not string_object.isalnum():
        assert_fail_message(when_failure_print_message)


def assert_str_is_not_alnuma(string_object: str, when_failure_print_message: str):
    if string_object.isalnum():
        assert_fail_message(when_failure_print_message)
