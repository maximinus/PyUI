import pygame
import unittest

from pyui.assets import file_cache
from pyui.helpers import Position, Mouse


class PyuiTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.mouse = Mouse()

    @classmethod
    def setUpClass(cls):
        # Initialize pygame and create a test surface
        pygame.init()
        pygame.display.set_mode((200, 200))

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
        
    def create_mouse(self, x: int = 0, y: int = 0, left: bool = False, 
                     middle: bool = False, right: bool = False) -> Mouse:
        """Create a mouse object with the given position and button states."""
        mouse = Mouse()
        mouse.update((x, y), (left, middle, right))
        return mouse
