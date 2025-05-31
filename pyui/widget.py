import pygame
from pygame import Surface

from pyui.messaging import message_bus
from pyui.helpers import Size, Margin, Align, Position, Expand, Mouse


class ImageCache:
    def __init__(self, image: Surface, size: Size): 
        self.image = image
        self.size = size

    def update(self, new_image: Surface):
        self.image = new_image
        self.size = Size(new_image.get_width(), new_image.get_height())
    
    def clear(self):
        self.image = None
        self.size = None

    def matches(self, size: Size) -> bool:
        if self.image is None or self.size is None:
            return False
        return self.size == size


class Widget:
    def __init__(self, margin=None, align=None, expand=None, background=None):
        if margin is None:
            margin = Margin()
        if align is None:
            align = Align(Align.CENTER, Align.CENTER)
        if expand is None:
            expand = Expand.NONE
        self.align = align
        self.margin = margin
        self.expand = expand
        self.background = background
        self.parent = None
        self.image = ImageCache(None, None)
        self.modal = False

    @property
    def min_size(self) -> Size:
        return Size(0, 0) + self.margin.size

    def get_new_image(self, size: Size) -> Surface:
        # The surface needs to have alpha
        new_surface = Surface((size.width, size.height), flags=pygame.SRCALPHA)
        if self.background is not None:
            new_surface.fill(self.background)
        return new_surface

    def get_position(self, area: Size) -> Position:
        render_position = Position(0, 0)
        space_x = area.width - self.min_size.width
        space_y = area.height - self.min_size.height
        # not enough space, render at 0,0
        if space_x < 0 or space_y < 0:
            return render_position
        # calculate position based on alignment
        # don't offset if wanting to expand AND self-expanding
        if space_x > 0:
            match self.align.horizontal:
                case Align.LEFT:
                    render_position.x = 0
                case Align.RIGHT:
                    render_position.x = space_x
                case Align.FILL:
                    render_position.x = 0
                case _:
                    render_position.x = space_x // 2
        if space_y > 0:
            match self.align.vertical:
                case Align.TOP:
                    render_position.y = 0
                case Align.BOTTOM:
                    render_position.y = space_y
                case Align.FILL:
                    render_position.y = 0
                case _:
                    render_position.y = space_y // 2
        return render_position

    def is_mouse_over(self, mouse: Mouse, pos: Position, size: Size) -> bool:
        """
        Check if mouse is over the widget's actual content area (excluding margins).
           Args:
             mouse: Tuple of (x, y) mouse coordinates
             pos: The position of the widget
             size: The size of the widget
           Returns:
             True if mouse is over the widget's content area
        """
        # Account for margins
        widget_xpos = pos.x + self.margin.left
        widget_ypos = pos.y + self.margin.top
    
        # Calculate actual content size (accounting for alignment)
        content_width = self.min_size.width - self.margin.width
        content_height = self.min_size.height - self.margin.height
    
        # Adjust content size based on alignment
        if self.align.horizontal == Align.FILL:
            content_width = size.width - self.margin.width
    
        if self.align.vertical == Align.FILL:
            content_height = size.height - self.margin.height
    
        # Check if mouse is within the content area
        return (widget_xpos <= mouse.position.x <= widget_xpos + content_width and 
                widget_ypos <= mouse.position.y <= widget_ypos + content_height)

    def render(self, mouse, surface: Surface, pos: Position, size: Size):
        pass

    def __del__(self):
        # Important: unsubscribe from all events
        message_bus.unsubscribe(self)
