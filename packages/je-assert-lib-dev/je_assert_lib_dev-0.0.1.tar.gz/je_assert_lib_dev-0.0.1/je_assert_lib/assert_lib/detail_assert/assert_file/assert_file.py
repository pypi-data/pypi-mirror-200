from filecmp import cmp
from pathlib import Path

from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_file_equal(file1, file2, when_failure_print_message: str):
    if (cmp(file1, file2)) is False:
        assert_fail_message(when_failure_print_message)


def assert_file_not_equal(file1, file2, when_failure_print_message: str):
    if (cmp(file1, file2)) is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_exists(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.exists() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_exists(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.exists() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_file(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_file() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_file(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_file() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_dir(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_dir() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_dir(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_dir() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_fifo(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_fifo() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_fifo(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_fifo() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_absolute(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_absolute() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_absolute(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_absolute() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_as_posix(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.as_posix() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_as_not_posix(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.as_posix() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_as_uri(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.as_uri() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_as_not_uri(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.as_uri() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_mount(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_mount() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_mount(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_mount() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_block_device(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_block_device() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_block_device(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_block_device() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_char_device(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_char_device() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_char_device(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_char_device() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_relative_to(assert_path: str, other: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_relative_to(other) is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_relative_to(assert_path: str, other: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_relative_to(other) is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_reserved(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_reserved() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_reserved(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_reserved() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_socket(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_socket() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_socket(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_socket() is True:
        assert_fail_message(when_failure_print_message)


def assert_path_is_symlink(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_symlink() is False:
        assert_fail_message(when_failure_print_message)


def assert_path_is_not_symlink(assert_path: str, when_failure_print_message: str):
    check_path = Path(assert_path)
    if check_path.is_symlink() is True:
        assert_fail_message(when_failure_print_message)
