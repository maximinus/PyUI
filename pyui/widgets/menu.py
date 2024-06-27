from pyui.base import get_asset, Size, Margin
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image, Spacer
from pyui.events.loop import app
from pyui.events.events import Event


class MenuItem(Widget):
    def __init__(self, text, icon_name=None):
        super().__init__()
        self.widget = HBox()
        if icon_name is not None:
            icon = Image(get_asset(f'icons/{icon_name}.png'), margin=Margin(2, 6, 4, 4))
            self.widget.add_widget(icon)
        else:
            self.widget.add_widget(Spacer(size=Size(22, 20)))
        self.widget.add_widget(TextLabel(text))
        self.size = self.widget.min_size
        self.highlighted = False

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        self.widget.render(surface, pos, available_size)
        self.render_rect = self.widget.render_rect
        self.redraw = False


class Menu(Border):
    def __init__(self, pos, items=None):
        box = VBox(margin=Margin(6, 6, 6, 6))
        if items is not None:
            for item in items:
                box.add_widget(item)
        super().__init__(pos, widget=box)
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
                print(f'Over menu {widget}')
                # update the new rect
                widget.highlighted = True
                app.set_dirty(widget)
                # can't be in the other widgets, so return early
                return
            # we are not over the menu item
            if widget.highlighted:
                print(f'Exited menu {widget}')
                widget.highlighted = False
                app.set_dirty(widget)
