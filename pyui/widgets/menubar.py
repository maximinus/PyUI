import pygame

from pyui.widgets import HBox, Label
from pyui.helpers import Margin, Align, Expand
from pyui.assets import get_font


class MenuItem(Label):
    """A menu item that can be clicked."""
    def __init__(self, text: str, font):
        super().__init__(text, font, (40, 40, 40), margin=Margin(12, 12, 5, 5))
    
    def render(self, mouse, destination, position, size):
        self.image.clear()
        if self.is_mouse_over(mouse, position, size):
            if mouse.left_click_down:
                print(f"Menu item '{self.text}' clicked")
            self.background = (100, 100, 100, 255)
        else:
            self.background = (0, 0, 0, 0)
        return super().render(mouse, destination, position, size)


class MenuBar(HBox):
    """A simple menu bar widget that can hold multiple menu items."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, align=Align(Align.FILL, Align.TOP),
                         expand=Expand.HORIZONTAL, **kwargs)
        self.font = get_font("creato.otf", 18)
    
    def add_menu(self, menu: str):
        label = MenuItem(menu, self.font)
        self.add_child(label)
    
    def render(self, mouse, destination, position, size):
        """Render the menu bar and its items."""
        if self.background is not None:
            pygame.draw.rect(destination, self.background,
                             (position.x, position.y, size.width, size.height))
        super().render(mouse, destination, position, size)
