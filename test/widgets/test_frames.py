import unittest

from pyui.base import Margin, Color, Size, Position
from pyui.widgets import Frame, ColorRect, Border
from test.sdl_test import SDLTest


class TestSimpleFrame(unittest.TestCase):
    def test_no_margin_size(self):
        frame = Frame(Size(0, 0))
        size = frame.min_size
        self.assertEqual(size.width, 0)
        self.assertEqual(size.height, 0)

    def test_with_frame(self):
        frame = Frame(Size(0, 0), margin=Margin(10, 10, 10, 10))
        size = frame.min_size
        self.assertEqual(size.width, 20)
        self.assertEqual(size.height, 20)

    def test_with_color_rect(self):
        frame = Frame(Size(0, 0), widget=ColorRect(Size(20, 20), Color.RED), margin=Margin(10, 10, 10, 10))
        size = frame.min_size
        # the frame min size always ignores the widget it contains
        self.assertEqual(size.width, 20)
        self.assertEqual(size.height, 20)

    def test_with_color_rect_and_margin(self):
        frame = Frame(Size(100, 100),
                      widget=ColorRect(Size(20, 20), Color.RED, margin=Margin(5, 5, 5, 5)),
                      margin=Margin(10, 10, 10, 10))
        size = frame.min_size
        self.assertEqual(size.width, 120)
        self.assertEqual(size.height, 120)


class TestSimpleBorder(SDLTest):
    def test_no_widgets_size(self):
        border = Border(Size(0, 0))
        self.assertEqual(border.current_size, Size(0, 0))

    def test_widget_size(self):
        border = Border(Size(20, 20), widget=ColorRect(Size(20, 20), Color.RED))
        min_size = border.min_size
        self.assertEqual(min_size.width, 20)
        self.assertEqual(min_size.height, 20)
