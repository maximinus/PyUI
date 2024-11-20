import pygame
import pygame.gfxdraw

from pyui.theme import THEME
from pyui.base import get_asset, Size, Position
from pyui.widget_base import Widget


# these items have a size, which is the size of the area to render other widgets
# since this size is fixed, the area given to child widgets is simply the size of the frame or border
# minus the margin
# it is an error to ask for a margin that is larger than the root size

class Root(Widget):
    def __init__(self, size, pos=None, modal=False, widget=None, margin=None, background=None):
        super().__init__(margin=margin)
        if pos is None:
            pos = Position(0, 0)
        self.position = pos
        self.modal = modal
        self.widget = widget
        if self.widget is not None:
            self.widget.parent = self
        self.parent = None
        if background is None:
            background = THEME.color['widget_background']
        self.background = background
        # if size is None, then assume the min size of the widget, or (0,0) if no widget
        if size is None:
            if widget is None:
                size = Size(0, 0)
            else:
                size = widget.min_size
        # the size we have must have the margin added
        self.current_size = size
        self.texture = None

    @property
    def container(self):
        return True

    @property
    def children(self):
        return [self.widget]

    @property
    def min_size(self):
        # the size includes the margin, as this is a fixed widget size
        return self.current_size

    def update_size(self, new_size):
        self.current_size = new_size
        self.draw(new_size)

    def draw(self, new_size):
        # frame sizes are fixed
        self.texture = self.get_texture(self.current_size)
        if self.background is not None:
            self.texture.fill(self.background)
        self.widget.render(self.current_size)

    def render(self, available_size, offset=Position(0, 0)):
        # available size is ignored here, we always fit the current size
        if self.texture is None:
            self.draw(self.current_size)

    def update_dirty_widget(self, widget):
        # either we contain this widget or not
        # drill down to find the widget
        original_widget = widget
        if widget.get_root() == self:
            # the first widget renders from its origin
            source_position = Position(0, 0)
            # where it goes to is the difference between the offsets
            dest_position = widget.frame_offset - widget.parent.frame_offset
            while widget.parent is not None:

                # If the widget has an alpha, it will merely draw over itself
                # So to do it properly, we need to render from the frame down
                # To do this, we need to clear the space under the blit area and put in our
                # background texture before we blit to the area

                # now we draw the widget texture part to the parent
                from_rect = pygame.Rect(source_position.x, source_position.y,
                                        original_widget.current_size.width, original_widget.current_size.height)

                # before we blit, take the area (dest.x, dest.y, from_rect.width, from rect.height),
                # clear it and add the background if we have one
                bg_rect = pygame.Rect(dest_position.x, dest_position.y, from_rect.width, from_rect.height)
                if self.background is None:
                    pygame.draw.rect(widget.parent.texture, (0, 0, 0, 0), bg_rect)
                else:
                    pygame.draw.rect(widget.parent.texture, self.background, bg_rect)

                widget.parent.texture.blit(widget.texture, (dest_position.x, dest_position.y), from_rect)
                source_position = dest_position
                dest_position += widget.parent.frame_offset
                widget = widget.parent
            # the area should be the size of the original widget
            return pygame.Rect(original_widget.frame_offset.x, original_widget.frame_offset.y,
                               original_widget.current_size.width, original_widget.current_size.height)
        else:
            # it's not us, but does it overlap us?
            area = pygame.Rect(self.position.x, self.position.y, self.current_size.width, self.current_size.height)
            collide_area = area.clip(area)
            if collide_area.size != 0:
                return collide_area


class Frame(Root):
    # a frame is a container that holds a single widget, and is a fixed size
    # the size does NOT include the margin; this means that if you set a frame to be 100x100 and it has a margin,
    # then the margin will decrease the effective size of the widget
    # a frame always needs a position
    def render(self, available_size=None, offset=Position(0, 0)):
        # the available size should be ignored with a frame; it is not sent from the top level,
        # and the size is fixed anyway
        self.texture = self.get_texture(self.current_size)
        if self.background is not None:
            self.texture.fill(self.background)

        if self.widget is not None:
            # since this is the root frame, the offset is just the margin
            self.widget.render(self.current_size)
            self.texture.blit(self.widget.texture, (0, 0))


class Border(Root):
    def __init__(self, size, pos=None, modal=False, background=None, widget=None):
        # the border contains another widget, however the default will be to grab the default size of the widget
        # there is a resize method if you want to change this
        # the actual size of the Border will be the child widget min size + border size
        # the border size will depend on the size of the nine-patch
        # the widget render will occur at the corner of the child widget
        # any margin will be ignored
        self.image = get_asset('nine_patch/frame.png')
        self.corner = Size(8, 8)
        self.middle = Size(4, 8)
        super().__init__(size, pos=pos, modal=modal, background=background, widget=widget)
        # where we draw this widget is adjusted by the border
        # TODO: we should change so the size is adjusted so that it is a widget with an inside widget
        # and the size we automatically adjust

    def draw(self, new_size):
        # in this case the size of the widget does NOT include the border, as it surrounds the widget
        # so the texture size must also include this
        self.texture = self.get_texture(self.current_size)

        x = 0
        y = 0
        # the size of the area the widgets need
        render_size = self.min_size

        # draw the top left
        self.texture.blit(self.image, (x, y), (0, 0, self.corner.width, self.corner.height))
        # top right
        self.texture.blit(self.image, (x + render_size.width + self.corner.width, y),
                          (self.corner.width + self.middle.width, 0, self.corner.width, self.corner.height))
        # bottom left
        self.texture.blit(self.image, (x, y + self.corner.height + render_size.height),
                          (0, self.corner.height + self.middle.width, self.corner.width, self.corner.height))
        # bottom right
        self.texture.blit(self.image,
                          (x + render_size.width + self.corner.width, y + self.corner.height + render_size.height),
                          (self.corner.width + self.middle.width, self.corner.height + self.middle.width,
                           self.corner.height, self.corner.width))

        # draw the borders by using pygame.transform.smoothscale to create a new image and blitting that
        side_ypos = y + self.corner.height

        left_unscaled = pygame.Surface((self.middle.height, self.middle.width), pygame.SRCALPHA)
        left_unscaled.blit(self.image, (0, 0), (0, self.corner.height, self.middle.height, self.middle.width))
        left_side = pygame.transform.scale(left_unscaled, (self.middle.height, render_size.height))
        self.texture.blit(left_side, (x, side_ypos))

        right_unscaled = pygame.Surface((self.middle.height, self.middle.width), pygame.SRCALPHA)
        right_unscaled.blit(self.image, (0, 0),
                            (self.corner.width + self.middle.width, self.corner.height, self.middle.height, self.middle.width))
        right_side = pygame.transform.scale(right_unscaled, (self.middle.height, render_size.height))
        self.texture.blit(right_side, (x + self.corner.width + render_size.width, side_ypos))

        # then top and bottom
        top_unscaled = pygame.Surface((self.middle.width, self.middle.height), pygame.SRCALPHA)
        top_unscaled.blit(self.image, (0, 0), (self.corner.width, 0, self.middle.width, self.middle.height))
        top_side = pygame.transform.scale(top_unscaled, (render_size.width, self.middle.height))
        self.texture.blit(top_side, (x + self.corner.width, y))

        bottom_unscaled = pygame.Surface((self.middle.width, self.middle.height), pygame.SRCALPHA)
        bottom_unscaled.blit(self.image, (0, 0), (self.corner.width, self.corner.height + self.middle.width, self.middle.width, self.middle.height))
        bottom_side = pygame.transform.scale(bottom_unscaled, (render_size.width, self.middle.height))
        self.texture.blit(bottom_side, (x + self.corner.width, y + self.corner.height + render_size.height))

        # draw the middle
        x += self.corner.width
        y += self.corner.height

        if self.background is not None:
            pygame.draw.rect(self.texture, self.background, (x, y, render_size.width, render_size.height))
        # TODO: Fix this +2. It is to do with overlap on the 9-patch; we need to define a better 9-patch object
        if self.widget is not None:
            self.widget.render(render_size)
            self.texture.blit(self.widget.texture, (x, y))

    def get_texture(self, size):
        # the texture size has to include the border margin
        border_size = self.corner.width * 2 + self.middle.width
        texture_size = size + Size(border_size, border_size)
        new_texture = pygame.Surface((texture_size.width, texture_size.height), pygame.SRCALPHA)
        return new_texture
