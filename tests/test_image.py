# filepath: /home/sparky/code/PyUI/tests/test_image.py
import unittest

import pygame
from pygame import Color, Surface

from pyui.widgets import Image
from pyui.helpers import Size, Margin, Position, Alignment, Expand
from pyui.test_helper import PyuiTest


class TestImage(unittest.TestCase):
    def test_image_creation(self):
        surface = Surface((50, 40))
        surface.fill(Color(255, 0, 0))
        image_widget = Image(image=surface)
        self.assertEqual(image_widget.size.width, 50)
        self.assertEqual(image_widget.size.height, 40)
    
    def test_size_with_margin(self):
        surface = Surface((50, 40))
        surface.fill(Color(255, 0, 0))
        image_widget = Image(image=surface, margin=Margin(10, 20, 30, 40))
        # min_size should include margins
        self.assertEqual(image_widget.min_size.width, 50 + 10 + 20)
        self.assertEqual(image_widget.min_size.height, 40 + 30 + 40)


class TestImageRendering(PyuiTest):
    def test_basic_render(self):
        img_surface = Surface((50, 50))
        img_surface.fill(Color(255, 0, 0))
        image_widget = Image(image=img_surface)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        # Check pixels (the image should be centered)
        self.assertPixel(dest_surface, Position(25, 25), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(74, 74), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(0, 0), Color(0, 0, 0))
        self.assertPixel(dest_surface, Position(75, 75), Color(0, 0, 0))
    
    def test_render_with_margin(self):
        img_surface = Surface((30, 30))
        img_surface.fill(Color(0, 255, 0))
        image_widget = Image(image=img_surface, margin=Margin(10, 10, 10, 10))
        dest_surface = pygame.Surface((50, 50))
        dest_surface.fill(Color(0, 0, 0))
        # Render the image (should respect margins)
        image_widget.render(dest_surface, Position(0, 0), Size(50, 50))
        self.assertPixel(dest_surface, Position(0, 0), Color(0, 0, 0))
        self.assertPixel(dest_surface, Position(10, 10), Color(0, 255, 0))
        self.assertPixel(dest_surface, Position(39, 39), Color(0, 255, 0))
        self.assertPixel(dest_surface, Position(40, 40), Color(0, 0, 0))
    
    def test_render_with_alignment_top_left(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(0, 0, 255))
        image_widget = Image(image=img_surface, align=Alignment.TOP_LEFT)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        self.assertPixel(dest_surface, Position(0, 0), Color(0, 0, 255))
        self.assertPixel(dest_surface, Position(39, 39), Color(0, 0, 255))
        self.assertPixel(dest_surface, Position(40, 40), Color(0, 0, 0))
    
    def test_render_with_alignment_top_right(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(255, 0, 0))
        image_widget = Image(image=img_surface, align=Alignment.TOP_RIGHT)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        self.assertPixel(dest_surface, Position(60, 0), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(99, 0), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(59, 0), Color(0, 0, 0))
    
    def test_render_with_alignment_bottom_left(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(0, 255, 0))
        image_widget = Image(image=img_surface, align=Alignment.BOTTOM_LEFT)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        self.assertPixel(dest_surface, Position(0, 60), Color(0, 255, 0))
        self.assertPixel(dest_surface, Position(0, 99), Color(0, 255, 0))
        self.assertPixel(dest_surface, Position(0, 59), Color(0, 0, 0))
    
    def test_render_with_alignment_bottom_right(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(0, 0, 255))
        image_widget = Image(image=img_surface, align=Alignment.BOTTOM_RIGHT)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        self.assertPixel(dest_surface, Position(60, 60), Color(0, 0, 255))
        self.assertPixel(dest_surface, Position(99, 99), Color(0, 0, 255))
        self.assertPixel(dest_surface, Position(59, 59), Color(0, 0, 0))
    
    def test_render_with_expand_horizontal(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(255, 0, 0))
        image_widget = Image(image=img_surface, expand=Expand.HORIZONTAL)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        # The image itself shouldn't expand, only the widget
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        # The image should still be 40x40 and centered vertically
        self.assertPixel(dest_surface, Position(30, 30), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(69, 69), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(70, 70), Color(0, 0, 0))
    
    def test_render_with_expand_vertical(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(0, 255, 0))
        image_widget = Image(image=img_surface, expand=Expand.VERTICAL)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        # The image itself shouldn't expand, only the widget
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        # The image should still be 40x40 and centered horizontally
        self.assertPixel(dest_surface, Position(30, 30), Color(0, 255, 0))
        self.assertPixel(dest_surface, Position(69, 69), Color(0, 255, 0))
        self.assertPixel(dest_surface, Position(70, 70), Color(0, 0, 0))
    
    def test_render_with_expand_both(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(0, 0, 255))
        image_widget = Image(image=img_surface, expand=Expand.BOTH)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        # The image itself shouldn't expand, only the widget
        image_widget.render(dest_surface, Position(0, 0), Size(100, 100))
        # The image should still be 40x40 and centered
        self.assertPixel(dest_surface, Position(30, 30), Color(0, 0, 255))
        self.assertPixel(dest_surface, Position(69, 69), Color(0, 0, 255))
        self.assertPixel(dest_surface, Position(70, 70), Color(0, 0, 0))
    
    def test_render_with_position_offset(self):
        img_surface = Surface((40, 40))
        img_surface.fill(Color(255, 0, 0))
        image_widget = Image(image=img_surface)
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        # Render the image with a position offset of (10, 10)
        image_widget.render(dest_surface, Position(10, 10), Size(80, 80))
        # The image should be centered within the 80x80 area at offset (10, 10)
        self.assertPixel(dest_surface, Position(10, 10), Color(0, 0, 0))
        self.assertPixel(dest_surface, Position(30, 30), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(69, 69), Color(255, 0, 0))
        self.assertPixel(dest_surface, Position(70, 70), Color(0, 0, 0))
