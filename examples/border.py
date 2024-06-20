import pygame
from pyui.setup import init, await_keypress

from pyui.base import Color, Size
from pyui.widgets import Border


if __name__ == '__main__':
    display = init()
    display.fill(Color.BACKGROUND)

    test_border = Border()
    test_border.render(display, 100, 100, Size(220, 80))

    pygame.display.flip()
    await_keypress()
    pygame.quit()
