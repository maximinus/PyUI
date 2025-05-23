import pygame
import unittest

from pyui.helpers import Position


class PyuiTest(unittest.TestCase):
    # helper class that sets up pygame for testing
    @classmethod
    def setUpClass(cls):
        pygame.init()
    
    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def assertPixel(self, surface: pygame.Surface, pos: Position, col: pygame.Color):
        # Test if a pixel at the given position is the expected color.
        pixel_color = surface.get_at((pos.x, pos.y))
        assert pixel_color == col, f"Pixel at {pos} is {pixel_color}, expected {col}"
    