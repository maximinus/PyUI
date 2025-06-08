import pygame
from pygame.surface import Surface

from pyui.assets import get_image, get_font
from pyui.widget import Widget
from pyui.helpers import Size, Position, Expand


class WindowImage:
    def __init__(self):
        self.top_left = get_image("left.png")
        self.top_middle = get_image("middle.png")
        self.top_right = get_image("right.png")


class WindowBar(Widget):
    """A window bar widget that can be used to create a custom window title bar."""
    def __init__(self, title: str):
        super().__init__(expand=Expand.HORIZONTAL)
        self.title = title
        self.background = (220, 200, 200)
        self.font = get_font("creato.otf", 18)
        self.gfx = WindowImage()

    @property
    def min_size(self) -> Size:
        """Calculate the minimum size of the window bar based on the title and graphics."""
        return Size(64, self.gfx.top_left.get_height())

    def render(self, mouse, destination: Surface, pos: Position, size: Size):
        if self.is_mouse_over(mouse, pos, size):
            # change to crosshair cursor when hovering over the title bar
            pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.image.matches(size):
            destination.blit(self.image.image, pos.as_tuple)
            return
        new_image = self.get_new_image(size)
        # top left
        new_image.blit(self.gfx.top_left, pos.as_tuple)
        xpos = self.gfx.top_left.get_width()
        right_edge = size.width - (self.gfx.top_right.get_width() + xpos + 64)
        while xpos < right_edge:
            new_image.blit(self.gfx.top_middle, (xpos, 0))
            xpos += 64
        # maybe some pixels left?
        width_left = (right_edge + 64 + self.gfx.top_right.get_width()) - xpos
        dest_rect = (0, 0, width_left, self.gfx.top_middle.get_height())
        new_image.blit(self.gfx.top_middle, (xpos, 0), dest_rect)
        new_image.blit(self.gfx.top_right, (size.width - self.gfx.top_right.get_width(), 0))
        text = self.font.render(self.title, (0, 0, 0))
        ypos = 16 - (text.get_height() // 2)
        xpos = (size.width // 2) - (text.get_width() // 2)
        new_image.blit(text, (xpos, ypos))
        destination.blit(new_image, pos.as_tuple)
        self.image.update(new_image)
