import pygame

from pyui.widgets import NinePatch, NinePatchData, ColorRect
from pyui.utility import wait_for_keypress
from pyui.helpers import Position, Size, Expand, Margin


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((350, 350))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))

    color_rect = ColorRect(color=(255, 0, 0),
                           size=Size(50, 50),
                           margin=Margin(10, 10, 10, 10))
    color_rect.render(screen, Position(0, 0), Size(70, 70))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
