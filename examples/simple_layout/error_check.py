import pygame

from pyui.widgets import Image
from pyui.utility import wait_for_keypress
from pyui.helpers import Margin, Position, Size, Expand


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((50, 50))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))


    img_surface = pygame.Surface((60, 60))
    img_surface.fill((0, 255, 0))
    image_widget = Image(image=img_surface)
    # Render the image with a position offset of (10, 10)
    image_widget.render(screen, Position(0, 0), Size(80, 80))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
