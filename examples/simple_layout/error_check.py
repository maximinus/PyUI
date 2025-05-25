import pygame

from pyui.widgets import ColorRect, HBox
from pyui.utility import wait_for_keypress
from pyui.helpers import Margin, Position, Size, Expand


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))

    box = HBox(spacing=0, margin=Margin(0, 0, 0, 0))
    box.add_child(ColorRect(color=(255, 0, 0), size=Size(20, 50), expand=Expand.HORIZONTAL))
    box.add_child(ColorRect(color=(0, 255, 0), size=Size(20, 50), expand=Expand.HORIZONTAL))
    box.render(screen, Position(0, 0), Size(100, 100))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
