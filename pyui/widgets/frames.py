import pygame
import pygame.gfxdraw

from pyui.theme import THEME
from pyui.base import get_asset, Size, Position
from pyui.widget_base import Widget


# these items have a size, which is the size of the area to render other widgets
# TODO: these widgets must have their own surface, which the child widgets render to
# this means that the positions for rendering must be realtive to the parent widget
# this makes dirty rect drawing a lot easier

class Root(Widget):
    def __init__(self, pos=None, modal=False, size=None, widget=None, margin=None, background=None):
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
        if size is None:
            # infer the size from the widget
            if widget is None:
                self.size = Size(0, 0)
            else:
                self.size = widget.min_size
        else:
            self.size = size
        self.texture = self.get_texture(self.size)

    @property
    def children(self):
        return [self.widget]

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def update_widget(self, widget):
        self.widget = widget
        self.size = widget.min_size()
        self.texture = self.get_texture()

    def update_size(self, new_size):
        self.size = new_size
        self.texture = self.get_texture()

    def draw(self, surface):
        self.render(surface, self.position, available_size=self.size)

    def update_dirty_rects(self, surface, dirty_rects):
        # TODO: This is going to need more work
        # Every widget will need to keep a copy of it's local render, and then we just draw all of those widgets
        # This ensure that everything renders correctly
        # Also, the root widget will need to apply it's background color at the start of this
        # When a widget says it is dirty, it should redraw itself to it's old render_rect settings

        # for each dirty rect, if our render_rect overlaps this rect, then update that part of the screen
        for dirty_rect in dirty_rects:
            if self.render_rect.colliderect(dirty_rect):
                # compute the clip area
                area_to_update = self.render_rect.clip(dirty_rect)
                # now blit from our texture to this screen
                source_area = area_to_update.copy()
                source_area.x -= self.position.x
                source_area.y -= self.position.y
                surface.blit(self.texture, (area_to_update.x, area_to_update.y), source_area)


class Frame(Root):
    # a frame is a container that holds a single widget, and is a fixed size
    # the size does NOT include the margin
    # a frame always needs a position
    def render(self, surface, _, available_size=None):
        if self.widget is None:
            return
        self.texture.fill(self.background)
        self.widget.render(self.texture, Position(0, 0), self.size)
        self.render_rect = self.widget.render_rect
        # now render to the screen
        surface.blit(self.texture, (self.position.x, self.position.y))


class Border(Root):
    def __init__(self, pos, modal=False, background=None, widget=None):
        # the border contains another widget, however the default will be to grab the default size of the widget
        # there is a resize method if you want to change this
        # the actual size of the Border will be the child widget min size + border size
        # the border size will depend on the size of the nine-patch
        # the widget render will occur at the corner of the child widget
        # any margin will be ignored
        self.image = get_asset('nine_patch/frame.png')
        self.corner = Size(8, 8)
        self.middle = Size(4, 8)
        super().__init__(pos, modal=modal, background=background, widget=widget)

    def render(self, surface, _, available_size=None):
        # on a full render of a border, we need to clear the texture as we blit alpha over it
        # if we just re-blit, we get the alphas blending together
        # as we are root, this is pretty easy
        self.texture = self.get_texture()
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

        pygame.draw.rect(self.texture, self.background, (x, y, render_size.width, render_size.height))
        # TODO: Fix this +2. It is to do with overlap on the 9-patch; we need to define a better 9-patch object
        border_size = self.corner.width + (self.middle.width // 2) - 2
        self.widget.render(self.texture, Position(border_size, border_size), render_size)
        self.render_rect = pygame.Rect(self.position.x, self.position.y, render_size.width, render_size.height)
        # finally, blit to screen
        surface.blit(self.texture, (self.position.x, self.position.y))

    def get_texture(self):
        # the texture size has to include the vorder margin
        border_size = self.corner.width * 2 + self.middle.width
        texture_size = self.size + Size(border_size, border_size)
        new_texture = pygame.Surface((texture_size.width, texture_size.height), pygame.SRCALPHA)
        return new_texture
