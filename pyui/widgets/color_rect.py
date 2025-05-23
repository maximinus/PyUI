import pygame
from pygame import Color, Surface

from pyui.widget import Widget
from pyui.helpers import Size, Position


class ColorRect(Widget):
    """
    A widget that displays a solid color rectangle.
    """
    def __init__(self, color: Color, size: Size, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.color = color

    @property
    def min_size(self) -> Size:
        return self.size + self.margin.size

    def render(self, destination: Surface, position: Position, size: Size):
        """
        Render the color rectangle to the given surface at the specified position.
        """
        render_pos = self.get_position(size)
        # add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        # draw the rectangle
        pygame.draw.rect(destination, self.color, (render_pos.x, render_pos.y, size.width, size.height))
