import unittest

from pyray import Color

from src.widgets import ColorRect
from src.helpers import Size, Margin


class TestColorRect(unittest.TestCase):
    def test_color(self):
        color_rect = ColorRect(color=Color(255, 0, 0), size=Size(0, 0))
        self.assertEqual(color_rect.color.r, 255)
        self.assertEqual(color_rect.color.g, 0)
        self.assertEqual(color_rect.color.b, 0)
    
    def test_size(self):
        color_rect = ColorRect(color=Color(0, 0, 0), size=Size(100, 200))
        self.assertEqual(color_rect.min_size.width, 100)
        self.assertEqual(color_rect.min_size.height, 200)
    
    def test_size_with_margin(self):
        color_rect = ColorRect(color=Color(0, 0, 0),
                               size=Size(100, 200), margin=Margin(10, 20, 30, 40))
        self.assertEqual(color_rect.min_size.width, 100 + 10 + 20)
        self.assertEqual(color_rect.min_size.height, 200 + 30 + 40)
