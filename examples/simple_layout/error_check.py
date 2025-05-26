import pygame

from pyui.widgets import NinePatch, NinePatchData
from pyui.utility import wait_for_keypress
from pyui.helpers import Margin, Position, Size, Expand


def run_example():
    pygame.init()
    screen = pygame.display.set_mode((350, 350))
    pygame.display.set_caption("Simple Color Rect Example")
    screen.fill((20, 20, 80))

    nine_patch_data = NinePatchData.from_json("button_test.json")
    nine_patch = NinePatch(nine_patch_data=nine_patch_data, expand=Expand.BOTH)
    # Render the image with a position offset of (10, 10)
    nine_patch.expand = Expand.BOTH
    nine_patch.render(screen, Position(0, 0), Size(80, 80))
    pygame.display.flip()

    wait_for_keypress()
    pygame.quit()


if __name__ == "__main__":
    run_example()
