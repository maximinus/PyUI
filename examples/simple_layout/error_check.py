import pygame

from pyui.widgets import Image
from pyui.utility import wait_for_keypress
from pyui.helpers import Position, Size, Expand, Margin


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((350, 350))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))

    img_surface = pygame.Surface((50, 50))
    img_surface.fill((255, 0, 0))
    image_widget = Image(image=img_surface)
    image_widget.render(screen, Position(0, 0), Size(100, 100))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
