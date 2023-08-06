from je_assert_lib import assert_str_is_alnum, assert_str_empty

assert_str_is_alnum("12345")

try:
    assert_str_empty("I'm not empty")
except AssertionError:
    print("That's right")
