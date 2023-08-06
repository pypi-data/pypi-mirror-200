from filecmp import cmp
from je_assert_lib.utils.assert_fail import assert_fail_message


def assert_file_equal(file1, file2,when_failure_print_message: str = None):
    if (cmp(file1, file2)) is False:
        assert_fail_message(when_failure_print_message)


def assert_file_not_equal(file1, file2,when_failure_print_message: str = None):
    if (cmp(file1, file2)) is True:
        assert_fail_message(when_failure_print_message)

