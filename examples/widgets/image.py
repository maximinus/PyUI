import pygame
from pyui.setup import init, await_keypress, DEFAULT_SIZE
from pyui.base import get_asset, Margin, Position, Size
from pyui.widgets import Image, Border

BACKGROUND_COLOR = (80, 80, 80)

# example functions to display Images


def screen1():
    texture = get_asset('images/dog.png')
    return Border(None, Position(100, 100), widget=Image(texture, margin=Margin(20, 20, 20, 20)))


def screen2():
    texture = get_asset('images/dog.png')
    return Border(None, Position(150, 150), widget=Image(texture, margin=Margin(60, 60, 60, 60)), background=(100, 100, 0))


if __name__ == '__main__':
    display = init()
    screens = [screen1(), screen2()]
    for single_screen in screens:
        display.fill(BACKGROUND_COLOR)
        single_screen.draw(Size(800, 600))
        display.blit(single_screen.texture, (100, 100))
        pygame.display.flip()
        await_keypress()
    pygame.quit()
