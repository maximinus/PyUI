import unittest

from pyui.base import Margin, Color, Size
from pyui.widgets import ColorRect


class TestColorRectMargins(unittest.TestCase):
    def test_horizontal_margins(self):
        rect = ColorRect(Size(100, 100), Color.RED, margin=Margin(5, 0, 5, 0))
        self.assertEqual(rect.min_size.width, 105)

    def test_vertical_margins(self):
        rect = ColorRect(Size(100, 100), Color.RED, margin=Margin(0, 5, 0, 5))
        self.assertEqual(rect.min_size.height, 105)

    def test_no_margins(self):
        rect = ColorRect(Size(100, 100), Color.RED, margin=Margin(0, 0, 0, 0))
        self.assertEqual(rect.min_size.width, 100)
        self.assertEqual(rect.min_size.height, 100)

    def test_both_margins(self):
        rect = ColorRect(Size(100, 100), Color.RED, margin=Margin(2, 3, 4, 5))
        self.assertEqual(rect.min_size.width, 105)
        self.assertEqual(rect.min_size.height, 109)
