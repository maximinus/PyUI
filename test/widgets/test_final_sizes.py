import pygame
import unittest

from pyui.base import Color, Size, Position, Expand, Margin
from pyui.setup import init
from pyui.widgets import ColorRect, Frame


# when a widget has some version of expand, a parent container will try to give as much as possible
# to that widget
# when a widget has some version of fill, it will "fill out" the widget if any space is given to it

class TestRenderSizes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_render_no_expand(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 100)
        self.assertEqual(color.render_rect.height, 100)

    def test_render_horizontal_expand(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.HORIZONTAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 200)
        self.assertEqual(color.render_rect.height, 100)

    def test_render_vertical_expand(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.VERTICAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 100)
        self.assertEqual(color.render_rect.height, 200)

    def test_render_both_expand(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.BOTH)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 200)
        self.assertEqual(color.render_rect.height, 200)

    def test_render_horizontal_fill(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, fill=Expand.HORIZONTAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 200)
        self.assertEqual(color.render_rect.height, 100)

    def test_render_vertical_fill(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, fill=Expand.VERTICAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 100)
        self.assertEqual(color.render_rect.height, 200)

    def test_render_both_fill(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, fill=Expand.BOTH)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 200)
        self.assertEqual(color.render_rect.height, 200)

    def test_render_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 100)
        self.assertEqual(color.render_rect.height, 100)

    def test_render_expand_horizontal_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.HORIZONTAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 180)
        self.assertEqual(color.render_rect.height, 100)

    def test_render_expand_vertical_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.VERTICAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 100)
        self.assertEqual(color.render_rect.height, 180)

    def test_render_expand_both_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.BOTH)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 180)
        self.assertEqual(color.render_rect.height, 180)

    def test_render_fill_horizontal_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, fill=Expand.HORIZONTAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 180)
        self.assertEqual(color.render_rect.height, 100)

    def test_render_fill_vertical_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, fill=Expand.VERTICAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 100)
        self.assertEqual(color.render_rect.height, 180)

    def test_render_fill_both_with_margin(self):
        display = init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.BOTH)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render(display, None, Size(200, 200))
        self.assertEqual(color.render_rect.width, 180)
        self.assertEqual(color.render_rect.height, 180)
