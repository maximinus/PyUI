import sys
import pygame
from pyui.base import Size
from pyui.theme import THEME

DEFAULT_SIZE = Size(800, 600)
CLOCK_FPS = 60


def get_clock():
    return pygame.time.Clock()


def init(size=DEFAULT_SIZE, title='PyUI'):
    pygame.init()
    screen = pygame.display.set_mode((size.width, size.height))
    pygame.display.set_caption(title)
    THEME.load_default()
    return screen


def await_keypress():
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            return


def await_end():
    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
