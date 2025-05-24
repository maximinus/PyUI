import pygame

from pyui.widgets import ColorRect
from pyui.utility import wait_for_keypress
from pyui.helpers import Margin, Position, Size, Alignment, Expand


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))

    rect = ColorRect(color=(255, 0, 0),
                     size=Size(50, 50),
                     margin=Margin(20, 20, 20, 20),
                     align=Alignment.TOP_LEFT,
                     expand=Expand.BOTH)
    rect.render(screen, Position(0, 0), Size(800, 600))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
