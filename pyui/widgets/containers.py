from pygame import Surface

from pyui.widget import Widget
from pyui.helpers import Size, Position

def split_pixels(total_children, spare_pixels):
    if total_children == 0:
        return []        
    # Base amount each child gets
    base = spare_pixels // total_children
    # Remaining pixels after even distribution
    remainder = spare_pixels % total_children    
    result = [base] * total_children
    # Distribute remaining pixels one by one
    for i in range(remainder):
        result[i] += 1
    return result

class HBox(Widget):
    """
    A horizontal box container that arranges its children in a single row.
    """
    def __init__(self, spacing: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.children = []
        self.spacing = spacing

    @property
    def min_size(self) -> Size:
        box_size = Size(0, 0)
        for child in self.children:
            child_size = child.min_size
            box_size.width += child_size.width
            box_size.height = max(box_size.height, child_size.height)
        total_children = len(self.children)
        if total_children > 1:
            box_size.width += total_children * self.spacing
        return box_size + self.margin.size

    def render(self, destination: Surface, pos: Position, size: Size):
        # the total size available for children is the size minus the margin
        available_size = size - self.margin.size
        spare_width = available_size.width - self.min_size.width
        if spare_width > 0:
            # we need to spread the spare width among the children
            total_expanding_children = 0
            for child in self.children:
                if child.expand.horizontal:
                    total_expanding_children += 1
            # decide how much to expand
            expansions = split_pixels(total_expanding_children, spare_width)
        else:
            expansions = [0] * len(self.children)
        # render each child
        current_x = pos.x + self.margin.left
        for i, child in enumerate(self.children):
            child_size = child.min_size
            if i > 0:
                current_x += self.spacing
            # expand the child if needed
            if child.expand.horizontal:
                child_size.width += expansions[i]
            # render the child
            child.render(destination, Position(current_x, pos.y + self.margin.top), child_size)
            current_x += child_size.width


class VBox(Widget):
    """
    A vertical box container that arranges its children in a single column.
    """
    def __init__(self, spacing: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.children = []
        self.spacing = spacing

    @property
    def min_size(self) -> Size:
        box_size = Size(0, 0)
        for child in self.children:
            child_size = child.min_size
            box_size.width = max(box_size.width, child_size.width)
            box_size.height += child_size.height
        total_children = len(self.children)
        if total_children > 1:
            box_size.height += total_children * self.spacing
        return box_size + self.margin.size

    def render(self, destination: Surface, pos: Position, size: Size):
        # the total size available for children is the size minus the margin
        available_size = size - self.margin.size
        spare_height = available_size.height - self.min_size.height
        if spare_height > 0:
            # we need to spread the spare height among the children
            total_expanding_children = 0
            for child in self.children:
                if child.expand.vertical:
                    total_expanding_children += 1
            # decide how much to expand
            expansions = split_pixels(total_expanding_children, spare_height)
        else:
            expansions = [0] * len(self.children)
        # render each child
        current_y = pos.y + self.margin.top
        for i, child in enumerate(self.children):
            child_size = child.min_size
            if i > 0:
                current_y += self.spacing
            # expand the child if needed
            if child.expand.vertical:
                child_size.height += expansions[i]
            # render the child
            child.render(destination, Position(pos.x + self.margin.left, current_y), child_size)
            current_y += child_size.height
