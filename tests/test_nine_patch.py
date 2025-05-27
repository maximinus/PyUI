import unittest

import pygame
from pygame import Color, Surface

from pyui.widgets import NinePatch, NinePatchData
from pyui.helpers import Size, Margin, Position, Align, Expand
from pyui.test_helper import PyuiTest


class TestNinePatchData(unittest.TestCase):
    def test_data_creation(self):
        nine_patch_data = NinePatchData(top=3, bottom=3, left=3, right=3)
        self.assertEqual(nine_patch_data.top, 3)
        self.assertEqual(nine_patch_data.bottom, 3)
        self.assertEqual(nine_patch_data.left, 3)
        self.assertEqual(nine_patch_data.right, 3)
        self.assertIsNone(nine_patch_data.image)
    
    def test_from_json(self):
        """Test loading NinePatchData from a JSON file"""
        nine_patch_data = NinePatchData.from_json("button.json")
        self.assertEqual(nine_patch_data.top, 3)
        self.assertEqual(nine_patch_data.bottom, 3)
        self.assertEqual(nine_patch_data.left, 3)
        self.assertEqual(nine_patch_data.right, 3)
        self.assertIsNotNone(nine_patch_data.image)
        self.assertIsInstance(nine_patch_data.image, Surface)
    
    def test_json_not_found(self):
        """Test error handling when JSON file is not found"""
        with self.assertRaises(FileNotFoundError):
            NinePatchData.from_json("nonexistent.json")


class TestNinePatch(unittest.TestCase):
    def setUp(self):
        self.nine_patch_data = NinePatchData.from_json("button.json")
        self.nine_patch = NinePatch(nine_patch_data=self.nine_patch_data)
    
    def test_nine_patch_creation(self):
        """Test basic creation of NinePatch widget"""
        self.assertEqual(self.nine_patch.nine_patch_data, self.nine_patch_data)
        self.assertEqual(self.nine_patch.render_image, self.nine_patch_data.image)
    
    def test_min_size(self):
        """Test minimum size calculation"""
        # Min size should be sum of left+right and top+bottom
        expected_min_width = self.nine_patch_data.left + self.nine_patch_data.right
        expected_min_height = self.nine_patch_data.top + self.nine_patch_data.bottom
        self.assertEqual(self.nine_patch.min_size.width, expected_min_width)
        self.assertEqual(self.nine_patch.min_size.height, expected_min_height)
    
    def test_min_size_with_margin(self):
        """Test minimum size calculation with margins"""
        nine_patch = NinePatch(nine_patch_data=self.nine_patch_data,
                               margin=Margin(10, 20, 30, 40))
        expected_min_width = self.nine_patch_data.left + self.nine_patch_data.right + 10 + 20
        expected_min_height = self.nine_patch_data.top + self.nine_patch_data.bottom + 30 + 40
        self.assertEqual(nine_patch.min_size.width, expected_min_width)
        self.assertEqual(nine_patch.min_size.height, expected_min_height)
    
    def test_expanding_property(self):
        """Test that NinePatch is self-expanding by default"""
        self.assertTrue(self.nine_patch.expanding)


class TestNinePatchRendering(PyuiTest):
    def setUp(self):
        self.nine_patch_data = NinePatchData.from_json("button_test.json")
        self.nine_patch = NinePatch(nine_patch_data=self.nine_patch_data)
    
    def test_basic_render(self):
        """Test basic rendering of a nine-patch"""
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        self.nine_patch.render(dest_surface, Position(0, 0), Size(50, 50))
        # The nine-patch should be rendered in the center
        # Check that the surface is modified from the original black
        self.assertNotPixel(dest_surface, Position(25, 25), (0, 0, 0))
    
    def test_render_with_margin(self):
        """Test rendering with margins"""
        nine_patch = NinePatch(nine_patch_data=self.nine_patch_data,
                               margin=Margin(10, 10, 10, 10))
        dest_surface = pygame.Surface((70, 70))
        dest_surface.fill(Color(0, 0, 0))
        nine_patch.render(dest_surface, Position(0, 0), Size(70, 70))
        self.assertPixel(dest_surface, Position(5, 5), (0, 0, 0))
        # Center area should be modified
        self.assertNotPixel(dest_surface, Position(35, 35), (0, 0, 0))
    
    def test_render_with_alignment_top_left(self):
        """Test rendering with top-left alignment"""
        nine_patch = NinePatch(nine_patch_data=self.nine_patch_data,
                               align=Align(Align.LEFT, Align.TOP))
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill((0, 0, 0))
        nine_patch.render(dest_surface, Position(0, 0), Size(50, 50))
        # Top-left area should be modified
        self.assertNotPixel(dest_surface, Position(5, 5), (0, 0, 0))
        # Bottom-right should be black (outside nine-patch)
        self.assertPixel(dest_surface, Position(75, 75), (0, 0, 0))
    
    def test_render_with_alignment_bottom_right(self):
        """Test rendering with bottom-right alignment"""
        nine_patch = NinePatch(nine_patch_data=self.nine_patch_data,
                               align=Align(Align.RIGHT, Align.BOTTOM))
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill((0, 0, 0))
        # Render at bottom-right of a 50x50 area
        nine_patch.render(dest_surface, Position(0, 0), Size(50, 50))
        
        # Bottom-right of the 50x50 area should be modified
        self.assertNotPixel(dest_surface, Position(45, 45), (0, 0, 0))
        # Top-left should be black (outside nine-patch)
        self.assertPixel(dest_surface, Position(5, 5), (0, 0, 0))
    
    def test_expanding_behavior(self):
        """Test that the nine-patch expands to fill available space"""
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        
        # Render at a size much larger than the original image
        self.nine_patch.expand = Expand.BOTH
        old_align = self.nine_patch.align
        self.nine_patch.align = Align(Align.FILL, Align.FILL)
        self.nine_patch.render(dest_surface, Position(0, 0), Size(80, 80))
        self.nine_patch.expand = Expand.NONE
        self.nine_patch.align = old_align

        # Check that the nine-patch expanded to fill most of the space
        self.assertNotPixel(dest_surface, Position(10, 10), (0, 0, 0))
        self.assertNotPixel(dest_surface, Position(70, 10), (0, 0, 0))
        self.assertNotPixel(dest_surface, Position(10, 70), (0, 0, 0))
        self.assertNotPixel(dest_surface, Position(70, 70), (0, 0, 0))
        # Check center
        self.assertNotPixel(dest_surface, Position(40, 40), (0, 0, 0))
    
    def test_render_with_position_offset(self):
        """Test rendering with a position offset"""
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        
        # Render with a position offset of (20, 20)
        self.nine_patch.render(dest_surface, Position(20, 20), Size(50, 50))
        # The area before the offset should be black
        self.assertPixel(dest_surface, Position(15, 15), (0, 0, 0))
        # The area within the nine-patch after the offset should be modified
        self.assertNotPixel(dest_surface, Position(45, 45), (0, 0, 0))
    
    def test_minimum_size_enforcement(self):
        """Test that the nine-patch enforces its minimum size"""
        dest_surface = pygame.Surface((100, 100))
        dest_surface.fill(Color(0, 0, 0))
        
        # Try to render at a size smaller than the minimum
        min_width = self.nine_patch_data.left + self.nine_patch_data.right
        min_height = self.nine_patch_data.top + self.nine_patch_data.bottom
        small_size = Size(min_width - 2, min_height - 2)
        # Should still render at minimum size
        self.nine_patch.render(dest_surface, Position(0, 0), small_size)        
        # Verify that minimum size was enforced by checking if pixels just outside
        # the requested small size were modified
        self.assertNotPixel(dest_surface, Position(min_width - 1, min_height - 1), (0, 0, 0))
