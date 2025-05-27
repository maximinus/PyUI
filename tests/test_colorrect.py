import unittest

import pygame
from pygame import Color

from pyui.widgets import ColorRect
from pyui.helpers import Size, Margin, Position, Align, Expand
from pyui.test_helper import PyuiTest


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
    
    def test_align_raises_assertion(self):
        with self.assertRaises(AssertionError):
            ColorRect(color=Color(255, 0, 0), size=Size(50, 50),
                      align=Align(Align.LEFT, Align.TOP))


class TestColorRectSizes(PyuiTest):
    def test_size_horizontal(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               margin=Margin(10, 10, 10, 10))
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(10, 10), Color(255, 0, 0))
        self.assertPixel(surface, Position(60, 10), Color(0, 0, 0))
        
    def test_size_vertical(self):
        color_rect = ColorRect(color=Color(0, 255, 0),
                               size=Size(50, 50),
                               margin=Margin(10, 10, 10, 10))
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(10, 10), Color(0, 255, 0))
        self.assertPixel(surface, Position(10, 60), Color(0, 0, 0))
    
    def test_size_horizontal_expanded(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               margin=Margin(10, 10, 10, 10),
                               expand=Expand.HORIZONTAL)
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(10, 70), Color(0, 0, 0))
        self.assertPixel(surface, Position(70, 10), Color(255, 0, 0))

    def test_size_vertical_expanded(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               margin=Margin(10, 10, 10, 10),
                               expand=Expand.VERTICAL)
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(70, 10), Color(0, 0, 0))
        self.assertPixel(surface, Position(10, 70), Color(255, 0, 0))
    
    def test_size_both_expanded(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               margin=Margin(10, 10, 10, 10),
                               expand=Expand.BOTH)
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(10, 10), Color(255, 0, 0))
        self.assertPixel(surface, Position(70, 10), Color(255, 0, 0))
        self.assertPixel(surface, Position(10, 70), Color(255, 0, 0))


class TestColorRectRender(PyuiTest):
    def test_render(self):
        color_rect = ColorRect(color=Color(255, 0, 0), size=Size(50, 50))
        surface = pygame.Surface((50, 50))
        color_rect.render(surface, Position(0, 0), Size(50, 50))
        self.assertPixel(surface, Position(0, 0), Color(255, 0, 0))

    def test_render_with_margin(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               margin=Margin(10, 10, 10, 10))
        surface = pygame.Surface((70, 70))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(70, 70))
        self.assertPixel(surface, Position(0, 0), Color(0, 0, 0))
        self.assertPixel(surface, Position(10, 10), Color(255, 0, 0))
