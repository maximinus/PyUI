import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Expand, Size, Color, Align
from pyui.widgets import ColorRect, HBox

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # a single HBox filling all space, has 3 widgets: the middle does not fill vertically
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, expand=Expand.BOTH),
                        ColorRect(Size(50, 50), Color.GREEN, expand=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.BLUE, expand=Expand.BOTH)])
    return box


def screen2():
    # three ColorRects that do not expand and are in the center of the expanded hbox
    box = HBox(expand=Expand.BOTH,
               widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.CENTER),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER)])
    return box


def screen3():
    # as 2, but aligned left, middle and right
    box = HBox(expand=Expand.BOTH,
               widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.START),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.CENTER),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.END)])
    return box


if __name__ == '__main__':
    display = init()
    screens = [screen1(), screen2(), screen3()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(display, 0, 0, DEFAULT_SIZE)
        pygame.display.flip()
        await_keypress()
    pygame.quit()
