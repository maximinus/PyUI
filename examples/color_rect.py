import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Expand, Size, Color, Align, Margin, Position
from pyui.widgets import ColorRect, HBox, VBox

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # a single HBox filling all space, has 3 widgets: the middle does not fill vertically
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, expand=Expand.BOTH),
                        ColorRect(Size(50, 50), Color.GREEN, expand=Expand.HORIZONTAL, fill=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.BLUE, expand=Expand.BOTH)])
    return box


def screen2():
    # three ColorRects that expand and are in the center of the expanded hbox
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.CENTER, expand=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER, expand=Expand.HORIZONTAL)])
    return box


def screen3():
    # as 2, but aligned left, middle and right, and the left fills all it's space
    box = HBox(widgets=[ColorRect(Size(100, 150), Color.RED, align=Align.LEFT, expand=Expand.HORIZONTAL, fill=Expand.BOTH),
                        ColorRect(Size(100, 150), Color.GREEN, align=Align.CENTER, expand=Expand.HORIZONTAL),
                        ColorRect(Size(100, 150), Color.BLUE, align=Align.RIGHT, expand=Expand.HORIZONTAL)])
    return box


def screen4():
    # 3 rows of 3 ColorRects, the centre one fills, the rest are centered
    row1 = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH)])
    row2 = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH, fill=Expand.BOTH),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH)])
    row3 = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH)])
    return VBox(widgets=[row1, row2, row3])


def screen5():
    # 3x1 array, but give a margin of differing sizes to each, center vertically
    m = Margin(10, 10, 10, 10)
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER,
                                  expand=Expand.BOTH, fill=Expand.HORIZONTAL, margin=m),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER,
                                  expand=Expand.BOTH, fill=Expand.HORIZONTAL, margin=m),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.CENTER,
                                  expand=Expand.BOTH, fill=Expand.HORIZONTAL, margin=m)])
    return box


if __name__ == '__main__':
    display = init()
    screens = [screen5(), screen2(), screen3(), screen4(), screen5()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(display, Position(0, 0), DEFAULT_SIZE)
        pygame.display.flip()
        await_keypress()
    pygame.quit()
