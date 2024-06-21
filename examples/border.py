import pygame
from pyui.setup import init, await_keypress

from pyui.base import Color, Size, Margin
from pyui.widgets import Border, ColorRect


if __name__ == '__main__':
    display = init()
    display.fill(Color.BACKGROUND)

    test_border = Border(widget=ColorRect(Size(100, 100), Color.BLUE, margin=Margin(32, 32, 32, 32)))
    test_border.render(display, 100, 100, Size(220, 80))

    pygame.display.flip()
    await_keypress()
    pygame.quit()
