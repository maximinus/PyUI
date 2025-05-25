import pygame

from pyui.widgets import ColorRect, HBox
from pyui.utility import wait_for_keypress
from pyui.helpers import Margin, Position, Size


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))

    box = HBox(spacing=0, margin=Margin(20, 20, 20, 20))
    box.add_child(ColorRect(color=(200, 30, 30), size=Size(150, 150)))
    box.add_child(ColorRect(color=(30, 200, 30), size=Size(150, 150)))
    box.add_child(ColorRect(color=(30, 30, 200), size=Size(150, 150)))

    # since the default is centered, we should be in the middle of the screen
    box.render(screen, Position(0, 0), Size(800, 600))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
