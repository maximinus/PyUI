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
        self.current_size = size.add_margin(self.margin)
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
        widget_space = self.current_size.subtract_margin(self.margin)
        # when we draw, we need to tell the next widget where it is relative to us
        # so here, for example, we are telling the widget to render to the given position,
        # which is an offset into our texture: we also need to tell it where that is on screen
        screen_pos = Position(self.position.x + self.margin.left, self.position.y + self.margin.top)
        self.widget.render(widget_space, Position(self.margin.left, self.margin.top))

    def render(self, available_size, offset=Position(0, 0)):
        # available size is ignored here, we always fit the current size
        if self.texture is not None:
            self.draw(self.current_size)

    def update_dirty_rects(self, surface, dirty_rects):
        # When a widget says it is dirty, it should redraw itself to its old render_rect settings
        # this means that all widgets have updated themselves at this point in the code

        # to do this, we need to iterate through all the widgets and get them to update
        # this means that children widgets will need to also have this function
        # the widgets must be drawn from the closest to the furthest, so we draw the widgets as we see
        # them, followed by their children

        for dirty_rect in dirty_rects:
            # either it's in this frame or not
            if not self.render_rect.colliderect(dirty_rect):
                # nothing to do with us
                return
            overlap_area = self.render_rect.clip(dirty_rect)
            # if our widget is a container, drill down
            if self.widget.container:
                self.widget.update_dirty_rect(overlap_area)
            # and then just copy from this texture to our texture
            self.texture.blit(self.widget.texture, (overlap_area.x, overlap_area.y), overlap_area)
            # render that new area to the screen
            surface.blit(self.texture, (overlap_area.x, overlap_area.y), overlap_area)


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

        size_with_margin = self.current_size.subtract_margin(self.margin)
        # the effective render size is the size of the frame minus it's margin
        if self.widget is not None:
            # since this is the root frame, the offset is just the margin
            self.widget.render(size_with_margin, Position(self.margin.left, self.margin.top))
            self.texture.blit(self.widget.texture, (self.margin.left, self.margin.top))


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
        border_size = self.corner.width + (self.middle.width // 2) - 2
        if self.widget is not None:
            self.widget.render(render_size, Position(self.margin.left, self.margin.top))
            self.texture.blit(self.widget.texture, (x, y))

    def get_texture(self, size):
        # the texture size has to include the border margin
        border_size = self.corner.width * 2 + self.middle.width
        texture_size = size + Size(border_size, border_size)
        new_texture = pygame.Surface((texture_size.width, texture_size.height), pygame.SRCALPHA)
        return new_texture
