import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Expand, Size, Color, Align, Margin, Position
from pyui.widgets import ColorRect, HBox, VBox

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # a rect fills the whole screen
    return ColorRect(Size(100, 100), Color.RED, expand=Expand.BOTH,
                     background=Color.GREEN, margin=Margin(50, 50, 50, 50))


def screen2():
    # a rect is centered, but does not fill (the default is to align in the center)
    return ColorRect(Size(100, 100), Color.RED, background=Color.BLUE, margin=Margin(50, 50, 50, 50))


def screen3():
    # the rect is on the bottom right
    return ColorRect(Size(100, 100), Color.GREEN, align=Align.RIGHT|Align.BOTTOM,
                     background=Color.BLUE, margin=Margin(50, 50, 50, 50))


def screen4():
    # the rect is on the left middle
    return ColorRect(Size(100, 100), Color.GREEN, align=Align.LEFT | Align.CENTER,
                     background=Color.BLUE, margin=Margin(50, 50, 50, 50))


if __name__ == '__main__':
    display = init()
    screens = [screen4()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(DEFAULT_SIZE)
        display.blit(single_screen.texture, (0, 0))
        pygame.display.flip()
        await_keypress()
    pygame.quit()
