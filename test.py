# -*- coding: utf-8 -*-

from __future__ import with_statement

import unittest

from assert_changes import assert_changes, assert_constant


class AssertChangesTest(unittest.TestCase):

    def test_passes_if_equal_to_new(self):
        value = 123
        with assert_changes(lambda: value, new=lambda old: old + 1):
            value += 1

    def test_fails_if_not_equal_to_new(self):
        def no_change():
            value = 123
            with assert_changes(lambda: value, new=lambda old: old + 1):
                pass
        self.assertRaises(AssertionError, no_change)

    def test_passes_if_cmp_returns_True(self):
        value = 'AbcDef'
        with assert_changes(lambda: value,
                            cmp=lambda old, new: old.lower() == new.lower()):
            value = 'aBCdEF'

    def test_fails_if_cmp_returns_False(self):
        def unacceptable_change():
            value = 'AbcDef'
            with assert_changes(lambda: value,
                                cmp=lambda old, new: old.lower() == new.lower()):
                value = 'GhiJkl'
        self.assertRaises(AssertionError, unacceptable_change)


class AssertConstantTest(unittest.TestCase):

    def test_passes_if_value_does_not_change(self):
        value = 123
        with assert_constant(lambda: value):
            pass

    def test_passes_if_value_does_not_change(self):
        def changes():
            value = 123
            with assert_constant(lambda: value):
                value += 1
        self.assertRaises(AssertionError, changes)


if __name__ == '__main__':
    unittest.main()
