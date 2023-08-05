from collections import deque, defaultdict, OrderedDict, Counter, ChainMap

from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_is_deque(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not deque:
        assert_fail_message(when_failure_print_message)


def assert_is_not_deque(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is deque:
        assert_fail_message(when_failure_print_message)


def assert_is_defaultdict(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not defaultdict:
        assert_fail_message(when_failure_print_message)


def assert_is_not_defaultdict(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is defaultdict:
        assert_fail_message(when_failure_print_message)


def assert_is_ordereddict(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not OrderedDict:
        assert_fail_message(when_failure_print_message)


def assert_is_not_ordereddict(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is OrderedDict:
        assert_fail_message(when_failure_print_message)


def assert_is_counter(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Counter:
        assert_fail_message(when_failure_print_message)


def assert_is_not_counter(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Counter:
        assert_fail_message(when_failure_print_message)


def assert_is_chainmap(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not ChainMap:
        assert_fail_message(when_failure_print_message)


def assert_is_not_chainmap(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is ChainMap:
        assert_fail_message(when_failure_print_message)
