import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Expand, Size, Color, Align, Margin, Position
from pyui.widgets import ColorRect, HBox, VBox, Spacer

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # a single HBox filling all space, has 3 widgets: the middle does not fill vertically
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, expand=Expand.BOTH),
                        ColorRect(Size(50, 50), Color.GREEN, expand=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.BLUE, expand=Expand.BOTH)])
    return box


def screen2():
    # three ColorRects that expand and are in the center of the expanded hbox
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.CENTER, expand=Expand.HORIZONTAL),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER, expand=Expand.HORIZONTAL)],
               align=Align.CENTER, background=(255, 255, 0))
    return box


def screen3():
    # as 2, but aligned left, middle and right, and the left fills all it's space
    box = HBox(widgets=[ColorRect(Size(100, 150), Color.RED, align=Align.LEFT, expand=Expand.HORIZONTAL),
                        ColorRect(Size(100, 150), Color.GREEN, align=Align.CENTER, expand=Expand.HORIZONTAL),
                        ColorRect(Size(100, 150), Color.BLUE, align=Align.RIGHT, expand=Expand.HORIZONTAL)])
    return box


def screen4():
    # 3 rows of 3 ColorRects, the centre one fills, the rest are centered
    m = Margin(10, 10, 10, 10)
    row1 = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m),
                         Spacer(expand=Expand.HORIZONTAL),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m),
                         Spacer(expand=Expand.HORIZONTAL),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m)])
    row2 = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH, margin=m),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m)])
    row3 = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m),
                         Spacer(expand=Expand.HORIZONTAL),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m),
                         Spacer(expand=Expand.HORIZONTAL),
                         ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.NONE, margin=m)])
    return VBox(widgets=[row1, row2, row3])


def screen5():
    # 3x1 array, but give a margin of differing sizes to each, center vertically
    m = Margin(10, 10, 10, 10)
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH, margin=m),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.CENTER, expand=Expand.BOTH, margin=m),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.CENTER, expand=Expand.BOTH, margin=m)])
    return box


def screen6():
    # like 5, but with differing background colors
    # 3x1 array, but give a margin of differing sizes to each, center vertically
    m = Margin(20, 20, 20, 20)
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER, expand=Expand.BOTH,
                                  margin=m, background=(50, 50, 50)),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.TOP, expand=Expand.HORIZONTAL,
                                  margin=m, background=(100, 100, 100)),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.BOTTOM, expand=Expand.HORIZONTAL,#
                                  margin=m, background=(150, 150, 150))])
    return box


def screen7():
    # like 5, but with differing background colors
    # 3x1 array, but give a margin of differing sizes to each, center vertically
    m = Margin(20, 20, 20, 20)
    box = HBox(background=[0, 0, 50], align=Align.CENTER,
               widgets=[ColorRect(Size(50, 50), Color.RED, align=Align.CENTER,
                                  expand=Expand.NONE, margin=m, background=(50, 50, 50)),
                        ColorRect(Size(50, 50), Color.BLUE, align=Align.TOP,
                                  expand=Expand.HORIZONTAL, margin=m, background=(100, 100, 100)),
                        ColorRect(Size(50, 50), Color.GREEN, align=Align.BOTTOM,
                                  expand=Expand.NONE, margin=m, background=(150, 150, 150))])
    return box


if __name__ == '__main__':
    display = init()
    screens = [screen1(), screen2(), screen3(), screen4(), screen5(), screen6(), screen7()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(DEFAULT_SIZE)
        display.blit(single_screen.texture, (0, 0))
        pygame.display.flip()
        await_keypress()
    pygame.quit()
