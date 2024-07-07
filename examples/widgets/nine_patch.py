import pygame.display

from pyui.base import NinePatch, Size, Color
from pyui.setup import init, await_keypress
from pyui.widgets import Button


if __name__ == '__main__':
    display = init()
    button = Button(background=Color.BLUE)
    button.draw(Size(200, 200))
    display.blit(button.texture, (100, 100))
    pygame.display.flip()
    await_keypress()
