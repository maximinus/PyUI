import pygame
import unittest

from pyui.setup import init
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
        menu = Menu(items=[menu1, menu2, menu3])
        height = menu.min_size.height
        # must be a multiple of 3
        self.assertTrue((height % 3) == 0)
