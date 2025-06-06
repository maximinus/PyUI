import pygame

from pyui.assets import get_image
from pyui.utility import wait_for_keypress

# Show a borderless window
# When a key is pressed, the window will close.


class WindowImage:
    def __init__(self):
        self.top_left = get_image("left.png")
        self.top_middle = get_image("middle.png")
        self.top_right = get_image("right.png")

def draw_window(screen):
    images = WindowImage()
    # background
    title_height = images.top_left.get_height()
    pygame.draw.rect(screen, (220, 200, 200),
                     (0, title_height, screen.get_width(), screen.get_height() - title_height))
    # top left
    screen.blit(images.top_left, (0, 0))
    xpos = images.top_left.get_width()
    right_edge = screen.get_width() - (images.top_right.get_width() + xpos + 64)
    print(f"right edge: {right_edge}")
    while xpos < right_edge:
        print(xpos)
        screen.blit(images.top_middle, (xpos, 0))
        xpos += 64
    # maybe some pixels left?
    width_left = (right_edge + 64 + images.top_right.get_width()) - xpos
    dest_rect = (0, 0, width_left, images.top_middle.get_height())
    screen.blit(images.top_middle, (xpos, 0), dest_rect)
    screen.blit(images.top_right, (screen.get_width() - images.top_right.get_width(), 0))

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
draw_window(screen)

pygame.display.flip()
wait_for_keypress()
