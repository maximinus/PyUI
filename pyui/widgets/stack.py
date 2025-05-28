from pygame import Surface

from pyui.widget import Widget
from pyui.widgets.containers import Container
from pyui.helpers import Size, Position


class Stack(Container):
    """
    A container widget that stacks multiple widgets on top of each other.
    The last widget in the list will be drawn last (on top).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.children = []

    def add_child(self, child: Widget):
        # Set child's background to None as per requirements
        child.background = None
        super().add_child(child)

    @property
    def min_size(self) -> Size:
        """
        The minimum size is the size of the largest child widget plus margins.
        """
        box_size = Size(0, 0)
        for child in self.children:
            child_size = child.min_size
            box_size.width = max(box_size.width, child_size.width)
            box_size.height = max(box_size.height, child_size.height)
        return box_size + self.margin.size

    def render(self, destination: Surface, pos: Position, size: Size):
        new_image = self.get_new_image(size)
        if self.background is not None:
            new_image.fill(self.background)
        # The total size available for children is the size minus the margin
        available_size = size - self.margin.size
        margin_pos = Position(self.margin.left, self.margin.top)
        for child in self.children:
            child.render(new_image, margin_pos, available_size)
        destination.blit(new_image, pos.as_tuple)
