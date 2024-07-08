import pygame

from pyui.base import Size, get_asset
from pyui.events.events import Event
from pyui.events.loop import app
from pyui.theme import THEME
from pyui.widget_base import Widget
from pyui.widgets import TextLabel


class NinePatch(Widget):
    def __init__(self, patch_name, min_size, **kwargs):
        # 9 patch is stored in 2 files: the image and the data
        # 9 patch essentially ignores expand: it always expands
        super().__init__(**kwargs)
        data = get_asset(f'nine_patch/{patch_name}.json')
        self.top = data['top']
        self.bottom = data['bottom']
        self.left = data['left']
        self.right = data['right']
        self.size = Size(data['width'], data['height'])
        self.image = get_asset(f'nine_patch/{patch_name}.png')
        self.patch_background = data['background']
        self.minimum_size = min_size

    @property
    def min_size(self):
        return self.minimum_size

    def draw(self, new_size):
        self.current_size = new_size
        # TODO: Add margin calculations

        self.texture = pygame.Surface((new_size.width, new_size.height), pygame.SRCALPHA)
        if self.patch_background is not None:
            pygame.draw.rect(self.texture, self.patch_background, (1, 1, new_size.width - 2, new_size.height - 2))

        # draw the corners
        self.texture.blit(self.image, (0, 0), (0, 0, self.left, self.top))
        self.texture.blit(self.image, (new_size.width - self.right, 0),
                         (self.size.width - self.right, 0, self.top, self.right))
        self.texture.blit(self.image, (0, new_size.height - self.bottom),
                         (0, self.size.height - self.bottom, self.left, self.bottom))
        self.texture.blit(self.image, (new_size.width - self.right, new_size.height - self.bottom),
                         (self.size.height - self.bottom, self.size.width - self.right, self.bottom, self.right))

        # draw the borders by using pygame.transform.smoothscale to create a new image and blitting that
        middle = Size(self.size.width - (self.left + self.right), self.size.height - (self.top + self.bottom))
        center_size = Size(new_size.width - (self.left + self.right), new_size.height - (self.top + self.bottom))

        left_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        left_unscaled.blit(self.image, (0, 0), (0, self.top, middle.width, middle.height))
        left_side = pygame.transform.scale(left_unscaled, (middle.width, center_size.height))
        self.texture.blit(left_side, (0, self.top))

        right_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        right_unscaled.blit(self.image, (0, 0),
                            (self.size.width - middle.width, self.top, middle.width, middle.height))
        right_side = pygame.transform.scale(right_unscaled, (middle.width, center_size.height))
        self.texture.blit(right_side, (new_size.width - middle.width, self.top))

        # top and bottom
        top_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        top_unscaled.blit(self.image, (0, 0), (self.left, 0, middle.width, middle.height))
        top_side = pygame.transform.scale(top_unscaled, (center_size.width, middle.height))
        self.texture.blit(top_side, (self.left, 0))

        bottom_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        bottom_unscaled.blit(self.image, (0, 0),
                             (self.left, self.size.height - 1, middle.width, middle.height))
        bottom_side = pygame.transform.scale(bottom_unscaled, (center_size.width, middle.height))

        self.texture.blit(bottom_side, (self.left, new_size.height - 1))


class StackBox(Widget):
    # renders things as a stack, from a -> b
    # we use as a tool for buttons
    # a text label sits on top of a nine-patch
    def __init__(self, widgets, **kwargs):
        super().__init__(**kwargs)
        # get the smallest size by finding the max size of the widgets
        self.widgets = widgets
        self.smallest_size = StackBox.get_largest_dimensions(self.widgets)

    @property
    def container(self):
        return True

    @property
    def children(self):
        return self.widgets

    @property
    def min_size(self):
        return self.smallest_size

    @classmethod
    def get_largest_dimensions(cls, widgets):
        largest = Size(0, 0)
        for widget in widgets:
            widget_size = widget.min_size
            largest.width = max(largest.width, widget_size.width)
            largest.height = max(largest.height, widget_size.height)
        return largest

    def draw(self, new_size):
        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)
        for widget in self.widgets:
            widget.render(new_size, offset=self.frame_offset)
            self.texture.blit(widget.texture, (0, 0))


class Button(StackBox):
    def __init__(self, text, min_size, **kwargs):
        self.normal_image = NinePatch('button', min_size)
        self.highlight_image = NinePatch('button_highlight', min_size)
        widgets = [self.normal_image, TextLabel(text=text, style=THEME.text['button_text'])]
        super().__init__(widgets=widgets, **kwargs)
        self.size = min_size
        # the button needs to connect to a few signals
        self.connect(Event.MouseIn, self.mouse_in)
        self.connect(Event.MouseOut, self.mouse_out)

    @property
    def min_size(self):
        return self.size

    def draw(self, new_size):
        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)

        offset = self.get_align_offset(self.size, new_size)

        for widget in self.widgets:
            widget.render(self.smallest_size, offset=self.frame_offset)
            self.texture.blit(widget.texture, (offset.x, offset.y))

        self.mouse_rect = pygame.Rect(self.frame_offset.x + offset.x, self.frame_offset.y + offset.y,
                                      new_size.width, new_size.height)

    def mouse_in(self, callback):
        self.widgets[0] = self.highlight_image
        self.draw(self.current_size)
        app.set_dirty(self)
        print('mouse_inside')

    def mouse_out(self, callback):
        self.widgets[0] = self.normal_image
        self.draw(self.current_size)
        app.set_dirty(self)
        print('mouse_outside')

    def button_clicked(self, callback):
        pass

    def button_click_release(self, callback):
        pass
