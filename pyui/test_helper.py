import pygame
import unittest

from pyui.assets import file_cache
from pyui.helpers import Position


class PyuiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize pygame and create a test surface
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        file_cache.clear()
        pygame.quit()

    def assertPixel(self, surface: pygame.Surface, pos: Position, col: pygame.Color):
        # Test if a pixel at the given position is the expected color.
        pixel_color = surface.get_at((pos.x, pos.y))
        assert pixel_color == col, f"Pixel at {pos} is {pixel_color}, expected {col}"
    
    def assertNotPixel(self, surface: pygame.Surface, pos: Position, col: pygame.Color):
        # Test if a pixel at the given position is NOT the expected color.
        pixel_color = surface.get_at((pos.x, pos.y))
        assert pixel_color != col, f"Pixel at {pos} is {pixel_color}, expected not {col}"
