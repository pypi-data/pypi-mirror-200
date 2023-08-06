def assert_fail_message(when_failure_print_message: str):
    if when_failure_print_message is None:
        when_failure_print_message = "Default assertion message"
    else:
        when_failure_print_message = str(when_failure_print_message)
    raise AssertionError(when_failure_print_message)
