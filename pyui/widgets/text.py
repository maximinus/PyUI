from pyui.widget import Widget


class TextArea(Widget):
    """A simple text area widget."""
    
    def __init__(self, text: str = "", font=None, color=(0, 0, 0), **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def render(self, mouse, destination, position, size):
        if self.font is None:
            return
        
        # Render the text using the font
        text_surface = self.font.render(self.text, True, self.color)
        destination.blit(text_surface, position)
