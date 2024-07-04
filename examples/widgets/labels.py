import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import Expand, Position, Align
from pyui.widgets import TextLabel, VBox, HBox
from pyui.theme import THEME

BACKGROUND_COLOR = (80, 80, 80)
# we will set up functions to display color widgets


def screen1():
    # 1 widget aligned to the centre of the screen
    return TextLabel('Hello, World!', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER)


def screen2():
    # a vbox with 3 centered labels of different sizes and colors
    box = VBox(widgets=[TextLabel('First label', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER),
                        TextLabel('Second label', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER),
                        TextLabel('Third label', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER)])
    return box


def screen3():
    # a hbox, 2 labels, aligned top to bottom
    box = HBox(widgets=[TextLabel('First label', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER|Align.TOP),
                        TextLabel('Second label', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER),
                        TextLabel('Third label', THEME.text['default'], expand=Expand.BOTH, align=Align.CENTER|Align.BOTTOM)])
    return box


def screen4():
    # a vbox with 3 centered labels of different sizes and colors, and also background colors
    box = VBox(widgets=[TextLabel('First label', THEME.text['default'], expand=Expand.BOTH,
                                  align=Align.CENTER, background=(0, 50, 50)),
                        TextLabel('Second label', THEME.text['default'], expand=Expand.BOTH,
                                  align=Align.CENTER, background=(0, 100, 100)),
                        TextLabel('Third label', THEME.text['default'], expand=Expand.BOTH,
                                  align=Align.CENTER, background=(0, 150, 150))])
    return box


if __name__ == '__main__':
    display = init()
    screens = [screen1(), screen2(), screen3(), screen4()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(display, Position(0, 0), Position(0, 0), DEFAULT_SIZE)
        pygame.display.flip()
        await_keypress()
    pygame.quit()
