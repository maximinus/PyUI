import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import get_asset, Margin, Position
from pyui.widgets import Image, Border

BACKGROUND_COLOR = (80, 80, 80)

# example functions to display Images


def screen1():
    texture = get_asset('images/dog.png')
    return Border(widget=Image(texture, margin=Margin(20, 20, 20, 20)))


if __name__ == '__main__':
    display = init()
    screens = [screen1()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.render(display, Position(100, 100), DEFAULT_SIZE)
        pygame.display.flip()
        await_keypress()
    pygame.quit()
