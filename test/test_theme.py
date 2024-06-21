import pygame
import unittest

from pyui.setup import init
from pyui.theme import THEME, TextStyle


class TestDefaultTheme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_colors(self):
        # no default colors
        self.assertEqual(len(THEME.colors), 0)

    def test_icons(self):
        # basic icon should be a surface
        self.assertEqual(len(THEME.icons), 1)
        self.assertTrue(isinstance(THEME.icons['open'], pygame.Surface))

    def test_text_type(self):
        self.assertEqual(len(THEME.text), 1)
        self.assertTrue(isinstance(THEME.text['menu'], TextStyle))

    def test_text_size(self):
        self.assertEqual(THEME.text['menu'].size, 24)

    def test_text_font(self):
        self.assertEqual(THEME.text['menu'].font, 'Inconsolata')

    def test_text_color(self):
        self.assertEqual(THEME.text['menu'].color, [20, 20, 20])

    def test_nine_patch(self):
        self.assertEqual(len(THEME.nine_patch), 2)

    def test_nine_patch_type(self):
        for _, value in THEME.nine_patch.items():
            self.assertTrue(isinstance(value, pygame.Surface))
