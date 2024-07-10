import pygame

from pyui.base import get_asset, Size, Margin, Expand, Align, Position
from pyui.theme import THEME
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image, Spacer
from pyui.events.loop import app
from pyui.events.events import Event


class MenuItem(Widget):
    def __init__(self, text, icon_name=None, style=None):
        super().__init__()
        self.widget = HBox()
        if icon_name is not None:
            icon = Image(get_asset(f'icons/{icon_name}.png'), margin=Margin(2, 6, 2, 2))
            self.widget.add_widget(icon)
        else:
            self.widget.add_widget(Spacer(size=Size(22, 20)))
        self.widget.add_widget(TextLabel(text, style=style, margin=Margin(0, 8, 0, 0)))
        self.size = self.widget.min_size
        self.highlighted = False
        self.connect(Event.MouseIn, self.mouse_in)
        self.connect(Event.MouseOut, self.mouse_out)

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def draw(self, new_size):
        self.texture = self.get_texture(new_size)

        if self.highlighted:
            self.texture.fill(THEME.color['menu_background'])
        elif self.background is not None:
            self.texture.fill(self.background)
        self.widget.draw(new_size)
        # render widget to me
        self.texture.blit(self.widget.texture, (self.margin.left, self.margin.top))
        self.widget_area = pygame.Rect(self.frame_offset.x, self.frame_offset.y, new_size.width, new_size.height)
        self.current_size = new_size

    def render(self, available_size, offset=Position(0, 0)):
        if available_size == self.current_size:
            return
        self.frame_offset = offset
        self.draw(available_size)

    def mouse_in(self, data):
        if self.highlighted:
            return
        self.highlighted = True
        self.draw(self.current_size)
        self.set_dirty()

    def mouse_out(self, data):
        if not self.highlighted:
            return
        self.highlighted = False
        self.draw(self.current_size)
        self.set_dirty()


def set_item_heights(items):
    if len(items) == 0:
        return []
    item_height = max([x.min_size.height for x in items])
    for item in items:
        height_diff = item_height - item.min_size.height
        if height_diff == 0:
            continue
        if height_diff % 2 == 1:
            height_diff -= 1
            item.margin.bottom += 1
        if height_diff > 0:
            height_div = height_diff // 2
            item.margin.top += height_div
            item.margin.bottom += height_div
    return items


class Menu(Border):
    def __init__(self, pos=None, items=None):
        box = VBox(margin=Margin(6, 6, 6, 6))
        if items is not None:
            for item in set_item_heights(items):
                box.add_widget(item)
        # menus are modal by default
        super().__init__(None, pos, widget=box, modal=True)

        self.connect(Event.MouseMove, self.mouse_move)
        # we also need to "cancel" the menu. This is done by clicking the main menu outside the box
        self.connect(Event.ClickOutside, self.cancel_menu)

    def add_menu_item(self, menu_item):
        self.widget.add_widget(menu_item)

    def cancel_menu(self, data):
        # this means there was a click, but not on our widget. It could have been any mouse click
        # we just need to close this modal frame
        app.remove_frame(self)

    def mouse_move(self, data):
        # called when we get a mouse move
        # return True to "consume", i.e., stop the event being sent anywhere else
        # we need to check if we are in or out of any vbox widgets
        for widget in self.widget.widgets:
            if widget.render_rect.collidepoint(data.event.xpos, data.event.ypos):
                # yes, we are over
                if widget.highlighted:
                    # nothing changed
                    return True
                # update the new rect
                widget.highlighted = True
                self.draw(self.current_size)
                app.set_dirty(widget)
                # don't return early, we still to check the other widgets
            else:
                # we are not over the menu item
                if widget.highlighted:
                    widget.highlighted = False
                    self.draw(self.current_size)
                    app.set_dirty(widget)


class MenuHeader(TextLabel):
    def __init__(self, text, menu):
        super().__init__(text, THEME.text['menu_header'], margin=Margin(6, 6, 4, 4), align=Align.CENTER)
        self.connect(Event.MouseLeftClickDown, self.clicked)
        assert isinstance(menu, Menu)
        self.menu = menu
        # we want a callback on this frame - we need to know when it is closed
        self.connect(Event.FrameClosed, self.menu_closed)
        self.menu_showing = False

    def get_menu_position(self):
        # TODO: Fix this
        return Position(50, 50)

    def clicked(self, event):

        print('Clicked')

        if self.menu_showing:
            # we are already open, ignore the click
            return
        # we don't really need the event
        # we update our highlight
        self.background = THEME.color['menu_header_highlight']
        self.draw(self.current_size)
        self.set_dirty()
        # we place a menu below us
        self.menu.position = self.get_menu_position()
        app.push_frame(self.menu)
        return True

    def menu_closed(self, event):
        if event.event.frame == self.menu:
            self.background = None
            self.set_dirty()


class MenuBar(HBox):
    def __init__(self, align=Align.TOP):
        super().__init__(expand=Expand.HORIZONTAL, background=THEME.color['menubar_background'], align=align)
        # to make the widget as big as possible, we put a spacer at the end with expand on
        self.add_widget(Spacer(Size(0, 0), expand=Expand.HORIZONTAL))

    def add_menu(self, text, menu):
        header_widget = MenuHeader(text, menu)
        header_widget.parent = self
        # we need to add the menu not at the end, but one before it
        # that way the spacer keeps to the right
        self.widgets.insert(len(self.widgets) - 1, header_widget)
        self.current_size = Size(0, 0)
        for widget in self.widgets:
            self.current_size += widget.min_size
