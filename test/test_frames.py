import pygame
import unittest

from pyui.setup import init
from pyui.base import Margin, Color, Size, Position
from pyui.widgets import Frame, ColorRect, Border


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


class TestSimpleBorder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_no_widgets_size(self):
        border = Border(Position(0, 0))
        self.assertEqual(border.size.width, 0)

    def test_widget_size(self):
        border = Border(Position(0, 0), widget=ColorRect(Size(20, 20), Color.RED))
        min_size = border.min_size
        self.assertEqual(min_size.width, 20)
        self.assertEqual(min_size.height, 20)
