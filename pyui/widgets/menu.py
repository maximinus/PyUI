from pyui.base import get_asset, Size, Margin, Expand, Align
from pyui.theme import THEME
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image, Spacer
from pyui.events.loop import app
from pyui.events.events import Event


class MenuItem(Widget):
    def __init__(self, text, icon_name=None, style=None):
        super().__init__()
        self.widget = HBox(fill=Expand.HORIZONTAL)
        if icon_name is not None:
            icon = Image(get_asset(f'icons/{icon_name}.png'), margin=Margin(2, 6, 2, 2))
            self.widget.add_widget(icon)
        else:
            self.widget.add_widget(Spacer(size=Size(22, 20)))
        self.widget.add_widget(TextLabel(text, style=style))
        self.size = self.widget.min_size
        self.highlighted = False

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        if self.highlighted:
            self.widget.background = THEME.color['menu_background']
        else:
            self.widget.background = THEME.color['widget_background']
        self.widget.render(surface, pos, available_size)
        self.render_rect = self.widget.render_rect


def set_item_heights(items):
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
    def __init__(self, pos, items=None):
        box = VBox(margin=Margin(6, 6, 6, 6))
        if items is not None:
            for item in set_item_heights(items):
                box.add_widget(item)
        # menus are modal by default
        super().__init__(pos, widget=box, modal=True)
        self.connect(Event.MouseMove, self.mouse_move)

    def add_menu_item(self, menu_item):
        self.widget.add_widget(menu_item)

    def mouse_move(self, event):
        # called when we get a mouse move
        # return True to "consume", i.e., stop the event being sent anywhere else
        # we need to check if we are in or out of any vbox widgets
        for widget in self.widget.widgets:
            if widget.render_rect.collidepoint(event.xpos, event.ypos):
                # yes, we are over
                if widget.highlighted:
                    # nothing changed
                    return True
                # update the new rect
                widget.highlighted = True
                app.set_dirty(widget)
                # don't return early, we still to check the other widgets
            else:
                # we are not over the menu item
                if widget.highlighted:
                    widget.highlighted = False
                    app.set_dirty(widget)


class MenuHeader(TextLabel):
    def __init__(self, text, menu):
        super().__init__(text, THEME.text['menu_header'], margin=Margin(6, 6, 4, 4), align=Align.CENTER)
        self.connect(Event.MouseLeftClickDown, self.clicked)
        self.menu = menu

    def clicked(self, event):
        print('I was clicked!')


class MenuBar(HBox):
    def __init__(self):
        super().__init__(expand=Expand.HORIZONTAL)
        self.background = THEME.color['menubar_background']

    def add_menu(self, text, menu):
        self.add_widget(MenuHeader(text, menu))
