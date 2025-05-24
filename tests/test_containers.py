import unittest

from pyui.widgets.containers import split_pixels


class TestSplitPixels(unittest.TestCase):
    def test_no_children(self):
        result = split_pixels(0, 10)
        self.assertEqual(result, [])

    def test_one_child(self):
        result = split_pixels(1, 10)
        self.assertEqual(result, [10])

    def test_two_children_even(self):
        result = split_pixels(2, 10)
        self.assertEqual(result, [5, 5])

    def test_two_children_odd(self):
        result = split_pixels(2, 11)
        self.assertEqual(result, [6, 5])

    def test_three_children_even(self):
        result = split_pixels(3, 12)
        self.assertEqual(result, [4, 4, 4])

    def test_three_children_odd(self):
        result = split_pixels(3, 13)
        self.assertEqual(result, [5, 4, 4])
