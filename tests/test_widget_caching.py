import pygame

from pyui.test_helper import PyuiTest
from pyui.helpers import Size, Position
from pyui.widgets import ColorRect


class TestWidgetCaching(PyuiTest):
    def test_initial_render_creates_cache(self):
        widget = ColorRect(color=(255, 0, 0), size=Size(50, 50))
        dest = pygame.Surface((100, 100))
        widget.render(dest, Position(0, 0), Size(100, 100))
        self.assertIsNotNone(widget.image.image)
        self.assertEqual(widget.image.size, Size(100, 100))
    
    def test_repeated_render_uses_cache(self):
        widget = ColorRect(color=(255, 0, 0), size=Size(50, 50))
        dest = pygame.Surface((100, 100))
        widget.render(dest, Position(0, 0), Size(100, 100))
        original_surface = widget.image.image
        widget.render(dest, Position(0, 0), Size(100, 100))
        # The cached surface should be the same object (not recreated)
        self.assertIs(widget.image.image, original_surface)
    
    def test_size_change_invalidates_cache(self):
        widget = ColorRect(color=(255, 0, 0), size=Size(50, 50))
        dest = pygame.Surface((200, 200))
        widget.render(dest, Position(0, 0), Size(100, 100))
        original_size = widget.image.size
        widget.render(dest, Position(0, 0), Size(150, 150))
        # The cached surface should be a different object
        self.assertNotEqual(widget.image.size, original_size)
        self.assertEqual(widget.image.size, Size(150, 150))
