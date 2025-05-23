from pygame import Surface

from src.widget import Widget
from src.helpers import Size, Position


class Image(Widget):
    """
    A widget that displays an image
    """
    def __init__(self, image: Surface, **kwargs):
        super().__init__(**kwargs)
        self.size = Size(image.get_width(), image.get_height())

    @property
    def min_size(self) -> Size:
        return self.size + self.margin.size

    def render(self, destination: Surface, position: Position, size: Size):
        """
        Render the image to the given surface at the specified position.
        """
        render_pos = self.get_position(size)
        # add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        # draw the rectangle
        destination.blit(self.image, (render_pos.x, render_pos.y))
