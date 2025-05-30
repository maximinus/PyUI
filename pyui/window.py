import pygame

from pyui.helpers import Size, Position, Mouse

FRAMES_PER_SECOND = 30


def pyui_init():
    if not pygame.get_init():
        pygame.init()


class Window:
    """
    A window class that manages multiple widgets.
    The window handles initialization, rendering, and the main event loop.
    Widgets are rendered in the order they were added (first to last).
    """
    def __init__(self, size: Size, background=(200, 200, 200), title: str = "PyUI Window"):
        pyui_init()
        self.title = title
        self.size = size
        self.widgets = []
        self.running = False
        self.background = background
        self.mouse = Mouse()
        
        current_surface = pygame.display.get_surface()
        if current_surface is not None:
            # If a surface already exists, we assume pygame is already initialized
            self.screen = current_surface
        else:
            pygame.display.set_caption(self.title)
            self.screen = pygame.display.set_mode(self.size.as_tuple)
   
    @classmethod
    def default(cls):
        """Create a default window with a size of 800x600."""
        return cls(Size(200, 200), title="Test Window")

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.parent = self
        
    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
            widget.parent = None
            
    def clear_widgets(self):
        for widget in self.widgets:
            widget.parent = None
        self.widgets = []

    def draw(self) -> None:
        """Clear the screen and draw all widgets in order."""
        self.screen.fill(self.background)
        for widget in self.widgets:
            widget.render(self.mouse, self.screen, Position(0, 0), self.size)
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        # Update mouse state
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        self.mouse.update(mouse_pos, mouse_buttons)
        
        # Process pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def run(self) -> None:
        """
        Start the main window loop.
        This will draw the window contents and handle events until the window is closed.
        """
        self.running = True
        
        self.draw()
        while self.running:
            self.running = self.handle_events()
            self.draw()
            # Control frame rate (60 FPS)
            pygame.time.Clock().tick(FRAMES_PER_SECOND)
        pygame.quit()
