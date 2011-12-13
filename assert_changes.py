"""
Track simple changes in values using context managers.
"""

from contextlib import contextmanager
import re


__all__ = ['assert_changes', 'assert_constant']


@contextmanager
def assert_changes(value_func, new=None, cmp=None, msg=None):

    """
    Assert that the value returned by `value_func()` changes in a certain way.

    `value_func()` needs to be a 0-ary callable which returns the monitored
    value. You can then specify either `new` or `cmp`, depending on the check
    you wish to perform.

    If `new` is provided, it should be an unary function. It will be called on
    the old value of `value_func()` and should return the expected new value.
    This expected value will be compared to the *actual* value after executing
    the body of the ``with`` block using a simple equality check. An
    AssertionError will be raised if the new value is not as expected.

    Alternatively, if `cmp` is provided, it should be a binary function over
    both the old and new values, returning ``True`` if the value changed as
    expected, or ``False`` otherwise. Note that it may also raise an
    ``AssertionError`` itself, so you could use a function like
    ``nose.tools.assert_greater_than()`` instead of ``operator.gt()``.

    Pass `msg` to override the default assertion message in the case of
    failure.
    """

    if cmp is None and new is None:
        raise TypeError("Requires either a `new` or `cmp` argument")
    elif not (cmp is None or new is None):
        raise TypeError("Cannot provide both `new` and `cmp` arguments")

    old_value = value_func()
    yield
    new_value = value_func()

    if new:
        expected_value = new(old_value)
        assert new_value == expected_value, (msg or
                "Value changed from %r to %r (expected: %r)" % (
                    new_value, old_value, expected_value))
    elif cmp:
        assert cmp(old_value, new_value), (msg or
                "%r(%r, %r) is not True" % (function_repr(cmp), old_value,
                                            new_value))


@contextmanager
def assert_constant(value_func, msg=None):

    """
    Assert that a monitored value does not change.

    `value_func` should return the monitored value. The new and old values will
    be compared via a simple equality check; if they are not equal, an
    AssertionError will be raised. Pass `msg` to override the default message.
    """

    old_value = value_func()
    yield
    new_value = value_func()
    assert new_value == old_value, (msg or
            "Value changed: from %r to %r" % (old_value, new_value))


def function_repr(func):

    """
    Get a more readable representation of a function object.

        >>> import operator
        >>> repr(operator.gt)
        '<built-in function gt>'
        >>> function_repr(operator.gt)
        'operator.gt'

        >>> repr('a'.lower)
        '<built-in method lower of str object at 0x...>'
        >>> function_repr('a'.lower)
        "'a'.lower"
    """

    initial_repr = repr(func)
    if not re.match(r'^\<.*\>$', initial_repr):
        return initial_repr

    if hasattr(func, '__self__'):
        return '%s.%s' % (repr(func.__self__), func.__name__)
    elif hasattr(func, '__module__'):
        return '%s.%s' % (func.__module__, func.__name__)
    else:
        return func.__name__
