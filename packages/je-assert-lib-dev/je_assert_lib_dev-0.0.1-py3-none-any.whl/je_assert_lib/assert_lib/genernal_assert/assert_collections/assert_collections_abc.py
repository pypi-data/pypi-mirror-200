from collections.abc import Awaitable, AsyncIterable, AsyncIterator, AsyncGenerator
from collections.abc import Collection, Coroutine, Callable, Container
from collections.abc import Iterator, Iterable, Generator, Reversible
from collections.abc import MappingView, KeysView, ItemsView, ValuesView
from collections.abc import Set, Mapping, MutableSet, MutableMapping, ByteString

from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_is_awaitable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Awaitable:
        assert_fail_message(when_failure_print_message)


def assert_is_not_awaitable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Awaitable:
        assert_fail_message(when_failure_print_message)


def assert_is_coroutine(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Coroutine:
        assert_fail_message(when_failure_print_message)


def assert_is_not_coroutine(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Coroutine:
        assert_fail_message(when_failure_print_message)


def assert_is_asynciterable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not AsyncIterable:
        assert_fail_message(when_failure_print_message)


def assert_is_not_asynciterable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is AsyncIterable:
        assert_fail_message(when_failure_print_message)


def assert_is_keysview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not KeysView:
        assert_fail_message(when_failure_print_message)


def assert_is_not_keysview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is KeysView:
        assert_fail_message(when_failure_print_message)


def assert_is_asyncgenerator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not AsyncGenerator:
        assert_fail_message(when_failure_print_message)


def assert_is_not_asyncgenerator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is AsyncGenerator:
        assert_fail_message(when_failure_print_message)


def assert_is_iterator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Iterator:
        assert_fail_message(when_failure_print_message)


def assert_is_not_iterator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Iterator:
        assert_fail_message(when_failure_print_message)


def assert_is_iterable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Iterable:
        assert_fail_message(when_failure_print_message)


def assert_is_not_iterable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Iterable:
        assert_fail_message(when_failure_print_message)


def assert_is_generator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Generator:
        assert_fail_message(when_failure_print_message)


def assert_is_not_generator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Generator:
        assert_fail_message(when_failure_print_message)


def assert_is_reversible(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Reversible:
        assert_fail_message(when_failure_print_message)


def assert_is_not_reversible(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Reversible:
        assert_fail_message(when_failure_print_message)


def assert_is_collection(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Collection:
        assert_fail_message(when_failure_print_message)


def assert_is_not_collection(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Collection:
        assert_fail_message(when_failure_print_message)


def assert_is_callable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Callable:
        assert_fail_message(when_failure_print_message)


def assert_is_not_callable(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Callable:
        assert_fail_message(when_failure_print_message)


def assert_is_container(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Container:
        assert_fail_message(when_failure_print_message)


def assert_is_not_container(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Container:
        assert_fail_message(when_failure_print_message)


def assert_is_set(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Set:
        assert_fail_message(when_failure_print_message)


def assert_is_not_set(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Set:
        assert_fail_message(when_failure_print_message)


def assert_is_mapping(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not Mapping:
        assert_fail_message(when_failure_print_message)


def assert_is_not_mapping(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is Mapping:
        assert_fail_message(when_failure_print_message)


def assert_is_mutableset(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not MutableSet:
        assert_fail_message(when_failure_print_message)


def assert_is_not_mutableset(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is MutableSet:
        assert_fail_message(when_failure_print_message)


def assert_is_mutablemapping(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not MutableMapping:
        assert_fail_message(when_failure_print_message)


def assert_is_not_mutablemapping(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is MutableMapping:
        assert_fail_message(when_failure_print_message)


def assert_is_bytestring(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not ByteString:
        assert_fail_message(when_failure_print_message)


def assert_is_not_bytestring(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is ByteString:
        assert_fail_message(when_failure_print_message)


def assert_is_mappingview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not MappingView:
        assert_fail_message(when_failure_print_message)


def assert_is_not_mappingview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is MappingView:
        assert_fail_message(when_failure_print_message)


def assert_is_itemsview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not ItemsView:
        assert_fail_message(when_failure_print_message)


def assert_is_not_itemsview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is ItemsView:
        assert_fail_message(when_failure_print_message)


def assert_is_valuesview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not ValuesView:
        assert_fail_message(when_failure_print_message)


def assert_is_not_valuesview(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is ValuesView:
        assert_fail_message(when_failure_print_message)


def assert_is_asynciterator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is not AsyncIterator:
        assert_fail_message(when_failure_print_message)


def assert_is_not_asynciterator(assert_object1, when_failure_print_message: str):
    if type(assert_object1) is AsyncIterator:
        assert_fail_message(when_failure_print_message)
