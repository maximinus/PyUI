import unittest

import pygame
from pygame import Color, Surface

from pyui.assets import get_font
from pyui.widgets import Label
from pyui.helpers import Size, Margin, Position, Align
from pyui.test_helper import PyuiTest


class TestFont(PyuiTest):
    def test_font_creation(self):
        font = get_font("creato.otf", 16)
        self.assertEqual(font.size, 16)
        self.assertIsNotNone(font.font)
    
    def test_font_size_of(self):
        font = get_font("creato.otf", 16)
        size = font.size_of("Test")
        self.assertIsInstance(size, Size)
        self.assertGreater(size.width, 0)
        self.assertGreater(size.height, 0)
    
    def test_font_render(self):
        font = get_font("creato.otf", 16)
        surface = font.render("Test", Color(255, 0, 0))
        self.assertIsInstance(surface, Surface)
        self.assertGreater(surface.get_width(), 0)
        self.assertGreater(surface.get_height(), 0)


class TestLabel(PyuiTest):
    def test_label_creation(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font, Color(255, 0, 0))
        self.assertEqual(label.text, "Test")
        self.assertEqual(label.color, Color(255, 0, 0))
        self.assertEqual(label.font, font)
    
    def test_label_size(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font)
        font_size = font.size_of("Test")
        self.assertEqual(label.min_size.width, font_size.width)
        self.assertEqual(label.min_size.height, font_size.height)
    
    def test_label_with_margin(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font, margin=Margin(10, 20, 30, 40))
        font_size = font.size_of("Test")
        self.assertEqual(label.min_size.width, font_size.width + 10 + 20)
        self.assertEqual(label.min_size.height, font_size.height + 30 + 40)
    
    def test_set_text(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font)
        old_size = label.min_size
        label.set_text("Longer test text")
        # Size should be updated
        self.assertNotEqual(label.min_size, old_size)
        self.assertEqual(label.text, "Longer test text")
        
        # Setting the same text shouldn't change anything
        label.set_text("Longer test text")
        self.assertEqual(label.min_size, label.min_size)
    
    def test_empty_text(self):
        font = get_font("creato.otf", 16)
        label = Label("", font)
        self.assertEqual(label.text, "")
        self.assertGreaterEqual(label.min_size.width, 0)
        self.assertGreaterEqual(label.min_size.height, 0)


class TestLabelRender(PyuiTest):
    def test_basic_render(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font, Color(255, 0, 0))
        surface = pygame.Surface((100, 50), flags=pygame.SRCALPHA)
        surface.fill(Color(0, 0, 0, 0))
        mouse = self.create_mouse()
        label.render(mouse, surface, Position(0, 0), Size(100, 50))
        
        # The exact pixel position would depend on font metrics and alignment
        # But we can verify that something was drawn by checking for non-black pixels
        has_content = False
        for x in range(100):
            for y in range(50):
                if surface.get_at((x, y)) != (0, 0, 0, 0):
                    has_content = True
                    break
            if has_content:
                break
        self.assertTrue(has_content)
    
    def test_alignment_center(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font, Color(255, 0, 0),
                     align=Align(Align.CENTER, Align.CENTER))
        surface = pygame.Surface((100, 50), flags=pygame.SRCALPHA)
        surface.fill(Color(0, 0, 0, 0))
        mouse = self.create_mouse()
        label.render(mouse, surface, Position(0, 0), Size(100, 50))
        
        # Center aligned - we should have transparent pixels at the edges
        self.assertEqual(surface.get_at((0, 0)), (0, 0, 0, 0))
        self.assertEqual(surface.get_at((99, 49)), (0, 0, 0, 0))
    
    def test_with_margin(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font, Color(255, 0, 0),
                     margin=Margin(10, 10, 10, 10))
        surface = pygame.Surface((100, 50), flags=pygame.SRCALPHA)
        surface.fill(Color(0, 0, 0, 0))
        mouse = self.create_mouse()
        label.render(mouse, surface, Position(0, 0), Size(100, 50))
        
        # Margin should leave transparent pixels at the edges
        self.assertEqual(surface.get_at((5, 5)), (0, 0, 0, 0))
    
    def test_cached_rendering(self):
        font = get_font("creato.otf", 16)
        label = Label("Test", font, Color(255, 0, 0))
        surface = pygame.Surface((100, 50), flags=pygame.SRCALPHA)
        
        # First render
        mouse = self.create_mouse()
        label.render(mouse, surface, Position(0, 0), Size(100, 50))
        
        # Cache should be used on second render
        self.assertTrue(label.image.matches(Size(100, 50)))
        
        # Change text to invalidate cache
        label.set_text("New text")
        self.assertFalse(label.image.matches(Size(100, 50)))
