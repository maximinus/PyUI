from pyray import Color

from src.widget import Widget
from src.helpers import Size


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
