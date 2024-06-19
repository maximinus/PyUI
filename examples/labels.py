import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Expand, Color, Align
from pyui.widgets import TextLabel, VBox, HBox

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # 1 widget aligned to the centre of the screen
    return TextLabel('Hello, World!', font_size=32, expand=Expand.BOTH, align=Align.CENTER)


def screen2():
    # a vbox with 3 centered labels of different sizes and colors
    box = VBox(widgets=[TextLabel('First label', font_size=20, color=Color.RED, expand=Expand.BOTH, align=Align.CENTER),
                        TextLabel('Second label', font_size=30, color=Color.GREEN, expand=Expand.BOTH, align=Align.CENTER),
                        TextLabel('Third label', font_size=40, color=Color.BLUE, expand=Expand.BOTH, align=Align.CENTER)])
    return box


def screen3():
    # a hbox, 2 labels, aligned top to bottom
    box = HBox(widgets=[TextLabel('First label', font_size=32, color=Color.RED, expand=Expand.BOTH, align=Align.CENTER|Align.TOP),
                        TextLabel('Second label', font_size=32, color=Color.GREEN, expand=Expand.BOTH, align=Align.CENTER),
                        TextLabel('Third label', font_size=32, color=Color.BLUE, expand=Expand.BOTH, align=Align.CENTER|Align.BOTTOM)])
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
