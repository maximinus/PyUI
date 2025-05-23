import unittest

import pygame
from pygame import Color

from pyui.widgets import ColorRect
from pyui.helpers import Size, Margin, Position, Alignment
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

    def test_render_to_center(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50))
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(0, 0), Color(0, 0, 0))
        self.assertPixel(surface, Position(25, 25), Color(255, 0, 0))

    def test_render_to_top_left(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               align=Alignment.TOP_LEFT)
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(0, 0), Color(255, 0, 0))
    
    def test_render_to_top_right(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               align=Alignment.TOP_RIGHT)
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(49, 0), Color(0, 0, 0))
        self.assertPixel(surface, Position(50, 0), Color(255, 0, 0))
    
    def test_render_to_bottom_left(self):
        color_rect = ColorRect(color=Color(255, 0, 0),
                               size=Size(50, 50),
                               align=Alignment.BOTTOM_LEFT)
        surface = pygame.Surface((100, 100))
        surface.fill(Color(0, 0, 0))
        color_rect.render(surface, Position(0, 0), Size(100, 100))
        self.assertPixel(surface, Position(0, 49), Color(0, 0, 0))
        self.assertPixel(surface, Position(0, 50), Color(255, 0, 0))
