import unittest
import pygame
from pyui.setup import init


class SDLTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.display = init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
