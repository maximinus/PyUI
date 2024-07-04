import unittest
from dataclasses import dataclass

import pygame
from pyui.setup import init


@dataclass
class FakeEvent:
    xpos: int
    ypos: int


class FakeTexture:
    def __init___(self):
        self.sdl_surface = None
        self.pos = None
        self.area = None
        self.fill_color = None
        self.blit_called = False
        self.fill_called = False

    def blit(self, surface, pos, area=None):
        self.sdl_surface = surface
        self.pos = pos
        self.area = area
        self.called = True

    def fill(self, color):
        self.fill_color = color
        self.fill_called = True


class SDLTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.display = init()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
