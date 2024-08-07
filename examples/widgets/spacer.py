import pygame
from pyui.setup import init, await_keypress
from pyui.base import Margin, Size, Color, Position
from pyui.widgets import ColorRect, HBox, Spacer, Border

BACKGROUND_COLOR = (80, 80, 80)

# we will set up functions to display color widgets


def screen1():
    # we will have the following
    # a border that holds a single hbox with 3 items: a color rect, spacer and another color rect
    # the color rects have a small margin
    box = HBox(widgets=[ColorRect(Size(50, 50), Color.BLUE, margin=Margin(10, 10, 10, 10)),
                        Spacer(Size(200, 0)),
                        ColorRect(Size(50, 50), Color.BLUE, margin=Margin(10, 10, 10, 10))])
    return Border(None, Position(100, 100), background=Color.BACKGROUND, widget=box)


if __name__ == '__main__':
    display = init()
    screens = [screen1()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.draw(display)
        display.blit(single_screen.texture, (0, 0))
        pygame.display.flip()
        await_keypress()
    pygame.quit()
