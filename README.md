# assert_changes

Track simple changes in values from the start to end of a context, and raise an
`AssertionError` if the final value was not as expected.

Simply pass `assert_changes()` two functions: one which returns a snapshot of
the monitored value, and another which represents the expected change.

You can also pass in a function which compares the old and new versions,
returning `True` if the change is acceptable and `False` otherwise. This allows
you to use operators other than simple equality for your tests.

## Installation

    pip install assert_changes

## Usage


Using the `new` parameter:

    >>> value = 123
    >>> with assert_changes(lambda: value, new=lambda x: x + 1):
    ...     value = 124
    
    >>> value = 123
    >>> with assert_changes(lambda: value, new=lambda x: x + 1):
    ...     value = 122
    Traceback (most recent call last):
    ...
    AssertionError: Value changed from 123 to 123 (expected: 124)

Using the `cmp` parameter:

    >>> import operator
    >>> value = 123
    >>> with assert_changes(lambda: value, cmp=operator.lt):
    ...     value += 4
    
    >>> value = 123
    >>> with assert_changes(lambda: value, cmp=operator.gt):
    ...     value += 4
    Traceback (most recent call last):
    ...
    AssertionError: operator.gt(123, 127) not True

You can even use an assertion as your comparison function:

    >>> value = 123
    >>> with assert_changes(lambda: value, cmp=assert_greater_than):
    ...     value += 4
    Traceback (most recent call last):
    ...
    AssertionError: 123 not greater than 127


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
