import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE

from pyui.base import Color, Size, Margin, Position
from pyui.widgets import Border, ColorRect


if __name__ == '__main__':
    display = init()
    display.fill(Color.BACKGROUND)

    test_border = Border(Position(100, 100),
                         widget=ColorRect(Size(100, 100), Color.BLUE, margin=Margin(32, 32, 32, 32)))
    test_border.draw(display)

    pygame.display.flip()
    await_keypress()
    pygame.quit()
