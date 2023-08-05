from sys import stderr


def assert_is_str(assert_object, when_failure_print_message: str):
    if type(assert_object) is not str:
        assert_fail_message(when_failure_print_message)


def assert_is_not_str(assert_object, when_failure_print_message: str):
    if type(assert_object) is str:
        assert_fail_message(when_failure_print_message)


def assert_is_int(assert_object, when_failure_print_message: str):
    if type(assert_object) is not int:
        assert_fail_message(when_failure_print_message)


def assert_is_not_int(assert_object, when_failure_print_message: str):
    if type(assert_object) is int:
        assert_fail_message(when_failure_print_message)


def assert_is_float(assert_object, when_failure_print_message: str):
    if type(assert_object) is not float:
        assert_fail_message(when_failure_print_message)


def assert_is_not_float(assert_object, when_failure_print_message: str):
    if type(assert_object) is float:
        assert_fail_message(when_failure_print_message)


def assert_is_complex(assert_object, when_failure_print_message: str):
    if type(assert_object) is not complex:
        assert_fail_message(when_failure_print_message)


def assert_is_not_complex(assert_object, when_failure_print_message: str):
    if type(assert_object) is complex:
        assert_fail_message(when_failure_print_message)


def assert_is_bytes(assert_object, when_failure_print_message: str):
    if type(assert_object) is not bytes:
        assert_fail_message(when_failure_print_message)


def assert_is_not_bytes(assert_object, when_failure_print_message: str):
    if type(assert_object) is bytes:
        assert_fail_message(when_failure_print_message)


def assert_is_bytearray(assert_object, when_failure_print_message: str):
    if type(assert_object) is not bytearray:
        assert_fail_message(when_failure_print_message)


def assert_is_not_bytearray(assert_object, when_failure_print_message: str):
    if type(assert_object) is bytearray:
        assert_fail_message(when_failure_print_message)
