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
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render()
        self.assertEqual(color.current_size.width, 100)
        self.assertEqual(color.current_size.height, 100)

    def test_render_horizontal_expand(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.HORIZONTAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render()
        self.assertEqual(color.current_size.width, 200)
        self.assertEqual(color.current_size.height, 100)

    def test_render_vertical_expand(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.VERTICAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render()
        self.assertEqual(color.current_size.width, 100)
        self.assertEqual(color.current_size.height, 200)

    def test_render_both_expand(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.BOTH)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200))
        frame.render()
        self.assertEqual(color.current_size.width, 200)
        self.assertEqual(color.current_size.height, 200)

    def test_render_with_margin(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render()
        self.assertEqual(color.current_size.width, 100)
        self.assertEqual(color.current_size.height, 100)

    def test_render_expand_horizontal_with_margin(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.HORIZONTAL)
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render()
        self.assertEqual(color.current_size.width, 200)
        self.assertEqual(color.current_size.height, 100)

    def test_render_expand_vertical_with_margin(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.VERTICAL)
        # the final size of the frame is the size passed + the margin
        frame = Frame(widget=color, pos=Position(0, 0), size=Size(200, 200), margin=Margin(10, 10, 10, 10))
        frame.render()
        self.assertEqual(color.current_size.width, 100)
        self.assertEqual(color.current_size.height, 200)

    def test_render_expand_both_with_margin(self):
        init(Size(200, 200))
        color = ColorRect(size=Size(100, 100), color=Color.RED, expand=Expand.BOTH)
        frame = Frame(Size(200, 200), widget=color, pos=Position(0, 0), margin=Margin(10, 10, 10, 10))
        frame.render()
        self.assertEqual(color.current_size.width, 200)
        self.assertEqual(color.current_size.height, 200)
