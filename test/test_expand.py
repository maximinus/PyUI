import unittest

from pyui.base import Expand


class TestExpand(unittest.TestCase):
    def test_none(self):
        exp = Expand.NONE
        self.assertFalse(exp.is_horizontal)
        self.assertFalse(exp.is_vertical)

    def test_horizontal(self):
        exp = Expand.HORIZONTAL
        self.assertTrue(exp.is_horizontal)
        self.assertFalse(exp.is_vertical)

    def test_vertical(self):
        exp = Expand.VERTICAL
        self.assertFalse(exp.is_horizontal)
        self.assertTrue(exp.is_vertical)

    def test_both(self):
        exp = Expand.BOTH
        self.assertTrue(exp.is_horizontal)
        self.assertTrue(exp.is_vertical)
