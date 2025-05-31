from pyui.helpers import Size
from pyui.widget import Widget


class Spacer(Widget):
    """A spacer widget that can be used to create empty space in a layout."""
    def __init__(self, expand):
        super().__init__(expand=expand)

    @property
    def min_size(self):
        return Size(0, 0)
    
    def render(self, mouse, surface, pos, size):
        pass
