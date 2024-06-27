import pygame
import unittest

from pyui.setup import init
from pyui.base import Position
from pyui.widgets import MenuItem, Menu


class TestMenuItem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_has_width(self):
        menu = MenuItem('Test')
        min_size = menu.min_size
        self.assertTrue(min_size.width > 0)
        self.assertTrue(min_size.height > 0)

    def test_equal_height(self):
        menu1 = MenuItem('Hello')
        menu2 = MenuItem('World')
        m1_size = menu1.min_size
        m2_size = menu2.min_size
        self.assertEqual(m1_size.height, m2_size.height)


class TestMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_equal_heights(self):
        menu1 = MenuItem('Hello')
        menu2 = MenuItem('World')
        menu3 = MenuItem('There')
        menu = Menu(Position(0, 0), items=[menu1, menu2, menu3])
        height = menu.min_size.height
        # must be a multiple of 3
        self.assertTrue((height % 3) == 0)


class TestSimpleCollision(unittest.TestCase):
    def test_simple_collision(self):
        render_rect = pygame.Rect(0, 0, 100, 100)
        self.assertTrue(render_rect.collidepoint(50, 50))

    def test_simple_collision_with_offset(self):
        render_rect = pygame.Rect(100, 100, 100, 100)
        self.assertTrue(render_rect.collidepoint(150, 150))

    def test_real_collision(self):
        # pygame seems funny about this
        # the rect is actually left, top, width, height
        render_rect = pygame.Rect(206, 156, 105, 24)
        # the collide_rect does not actually allow for the top and bottom, it checks against width and height
        self.assertTrue(render_rect.collidepoint(210, 160))

    def test_real_no_collision(self):
        render_rect = pygame.Rect(206, 156, 105, 24)
        self.assertFalse(render_rect.collidepoint(0, 0))
