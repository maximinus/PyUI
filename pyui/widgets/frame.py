import pygame
from pygame import Surface

from pyui.widget import Widget
from pyui.widgets.nine_patch import NinePatch, NinePatchData
from pyui.helpers import Size, Position, Expand

# Frames cannot cache their contents as the inner widgets may want to update

class Frame(Widget):
    """
    A widget that wraps a child widget in a nine-patch frame.
    The min size of the nine-patch is exactly that of the contained widget.
    It will fill if align.fill is set
    """
    def __init__(self, child: Widget, nine_patch_data: NinePatchData, **kwargs):
        super().__init__(**kwargs)
        self.child = child
        if child is not None:
            self.child.parent = self
        self.nine_patch_data = nine_patch_data
        # Don't create the NinePatch here as we need dynamic sizing based on the child

    @property
    def min_size(self) -> Size:
        # Frame size is child size plus the nine patch borders and padding
        n = self.nine_patch_data
        if self.child is None:
            frame_size = Size(n.left + n.right, n.top + n.bottom)
            return frame_size + self.margin.size
        child_size = self.child.min_size
        frame_size = Size(
            child_size.width + n.left + n.right,
            child_size.height + n.top + n.bottom
        )
        return frame_size + self.margin.size

    @property
    def has_child(self) -> bool:
        return self.child is not None

    def add_child(self, widget):
        widget.parent = self
        self.child = widget

    def get_new_image(self, size: Size) -> Surface:
        # The surface needs to have alpha
        return Surface((size.width, size.height), flags=pygame.SRCALPHA)

    def render_child(self, mouse, destination: Surface, position: Position, size: Size):
        """
        Render the child widget inside the frame.
        """
        if self.child is not None:
            self.render_child(mouse, destination, position, size)
            child_pos = Position(self.nine_patch_data.left, self.nine_patch_data.top)
            child_size = Size(
                size.width - self.nine_patch_data.left - self.nine_patch_data.right,
                size.height - self.nine_patch_data.top - self.nine_patch_data.bottom
            )
            self.child.render(mouse, destination, child_pos, child_size)

    def render(self, mouse, destination: Surface, position: Position, size: Size):
        """
        Render the nine patch frame and the child widget inside it.
        """
        if self.image.matches(size):
            destination.blit(self.image.image, position.as_tuple)
            self.render_child(mouse, destination, position, size)
            return

        new_image = self.get_new_image(size)
        render_pos = self.get_position(size)

        # Add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        
        # Calculate render size (subtract margins)
        render_width = self.min_size.width - self.margin.width
        if self.expand.horizontal:
            render_width = size.width - self.margin.width
        render_height = self.min_size.height - self.margin.height
        if self.expand.vertical:
            render_height = size.height - self.margin.height
        
        # Calculate size available for the nine patch
        frame_size = Size(render_width, render_height)

        # Create a temporary surface for the frame and child
        frame_surface = Surface(frame_size.as_tuple).convert_alpha()
        frame_surface.fill((0, 0, 0, 0))
        
        # Create a NinePatch with the correct size for this rendering
        n = self.nine_patch_data
        nine_patch = NinePatch(self.nine_patch_data, frame_size)
        nine_patch.render(mouse, frame_surface, Position(0, 0), frame_size)

        child_pos = Position(n.left, n.top)
        child_size = Size(
            frame_size.width - n.left - n.right,
            frame_size.height - n.top - n.bottom
        )
        
        # If background color is specified, draw a rectangle in the inner area
        if self.background is not None:
            pygame.draw.rect(frame_surface, self.background, 
                             (child_pos.x, child_pos.y, child_size.width, child_size.height))
        if self.child is not None:
            self.child.render(mouse, frame_surface, child_pos, child_size)
        new_image.blit(frame_surface, render_pos.as_tuple)
        destination.blit(new_image, position.as_tuple)
        self.render_child(mouse, destination, position, size)
        self.image.update(new_image)

    def set_active(self, is_active):
        self.active = is_active
        if self.child is not None:
            self.child.set_active(is_active)
