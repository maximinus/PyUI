import unittest

from pyui.base import Margin, Color, Size, Position
from pyui.widgets import Frame, ColorRect, Border
from test.sdl_test import SDLTest


class TestSimpleFrame(unittest.TestCase):
    def test_no_margin_size(self):
        frame = Frame(Position(0, 0))
        size = frame.min_size
        self.assertEqual(size.width, 0)
        self.assertEqual(size.height, 0)

    def test_with_frame(self):
        frame = Frame(Position(0, 0), margin=Margin(10, 10, 10, 10))
        size = frame.min_size
        self.assertEqual(size.width, 20)
        self.assertEqual(size.height, 20)

    def test_with_color_rect(self):
        frame = Frame(Position(0, 0), widget=ColorRect(Size(20, 20), Color.RED), margin=Margin(10, 10, 10, 10))
        size = frame.min_size
        self.assertEqual(size.width, 40)
        self.assertEqual(size.height, 40)

    def test_with_color_rect_and_margin(self):
        frame = Frame(Position(0, 0),
                      widget=ColorRect(Size(20, 20), Color.RED, margin=Margin(5, 5, 5, 5)),
                      margin=Margin(10, 10, 10, 10))
        size = frame.min_size
        self.assertEqual(size.width, 50)
        self.assertEqual(size.height, 50)


class TestSimpleBorder(SDLTest):
    def test_no_widgets_size(self):
        border = Border(Position(0, 0))
        self.assertEqual(border.size.width, 0)

    def test_widget_size(self):
        border = Border(Position(0, 0), widget=ColorRect(Size(20, 20), Color.RED))
        min_size = border.min_size
        self.assertEqual(min_size.width, 20)
        self.assertEqual(min_size.height, 20)


class TestFrameChildrenRenderRect(SDLTest):
    def test_child_location_at_origin(self):
        border = Frame(Position(0, 0), widget=ColorRect(Size(20, 20), Color.RED))
        border.render(self.__class__.display, None, None)
        color_area = border.widget.render_rect
        self.assertEqual(color_area.x, 0)
        self.assertEqual(color_area.y, 0)

    def test_child_location_at_offset(self):
        border = Frame(Position(50, 60), widget=ColorRect(Size(20, 20), Color.RED))
        border.render(self.__class__.display, None, None)
        color_area = border.widget.render_rect
        self.assertEqual(color_area.x, 50)
        self.assertEqual(color_area.y, 60)
