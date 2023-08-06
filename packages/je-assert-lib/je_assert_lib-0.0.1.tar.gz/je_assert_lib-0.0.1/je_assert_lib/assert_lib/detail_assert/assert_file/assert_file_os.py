from os import path

from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_file_exists(assert_path: str,when_failure_print_message: str = None):
    if path.exists(assert_path) is False:
        assert_fail_message(when_failure_print_message)


def assert_file_not_exists(assert_path: str,when_failure_print_message: str = None):
    if path.exists(assert_path) is True:
        assert_fail_message(when_failure_print_message)


def assert_is_dir(assert_path: str,when_failure_print_message: str = None):
    if path.isdir(assert_path) is False:
        assert_fail_message(when_failure_print_message)


def assert_is_not_dir(assert_path: str,when_failure_print_message: str = None):
    if path.isdir(assert_path) is True:
        assert_fail_message(when_failure_print_message)


def assert_is_abs(assert_path: str,when_failure_print_message: str = None):
    if path.isabs(assert_path) is False:
        assert_fail_message(when_failure_print_message)


def assert_is_not_abs(assert_path: str,when_failure_print_message: str = None):
    if path.isabs(assert_path) is True:
        assert_fail_message(when_failure_print_message)


def assert_is_file(assert_path: str,when_failure_print_message: str = None):
    if path.isfile(assert_path) is False:
        assert_fail_message(when_failure_print_message)


def assert_is_not_file(assert_path: str,when_failure_print_message: str = None):
    if path.isfile(assert_path) is True:
        assert_fail_message(when_failure_print_message)


def assert_is_link(assert_path: str,when_failure_print_message: str = None):
    if path.islink(assert_path) is False:
        assert_fail_message(when_failure_print_message)


def assert_is_not_link(assert_path: str,when_failure_print_message: str = None):
    if path.islink(assert_path) is True:
        assert_fail_message(when_failure_print_message)


def assert_is_mount(assert_path: str,when_failure_print_message: str = None):
    if path.ismount(assert_path) is False:
        assert_fail_message(when_failure_print_message)


def assert_is_not_mount(assert_path: str,when_failure_print_message: str = None):
    if path.ismount(assert_path) is True:
        assert_fail_message(when_failure_print_message)
