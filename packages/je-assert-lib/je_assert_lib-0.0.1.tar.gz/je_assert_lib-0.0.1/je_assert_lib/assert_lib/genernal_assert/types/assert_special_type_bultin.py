from functools import partial
from sys import stderr
from types import FunctionType, BuiltinFunctionType, LambdaType, MethodType


def assert_is_memoryview(assert_object,when_failure_print_message: str = None):
    if type(assert_object) is not memoryview:
        assert_fail_message(when_failure_print_message)


def assert_is_not_memoryview(assert_object,when_failure_print_message: str = None):
    if type(assert_object) is memoryview:
        assert_fail_message(when_failure_print_message)


def assert_is_function(function,when_failure_print_message: str = None):
    if not isinstance(
            function,
            (FunctionType, BuiltinFunctionType, partial, LambdaType, MethodType)
    ):
        assert_fail_message(when_failure_print_message)


def assert_is_not_function(function,when_failure_print_message: str = None):
    if isinstance(
            function,
            (FunctionType, BuiltinFunctionType, partial, LambdaType, MethodType)
    ):
        assert_fail_message(when_failure_print_message)
