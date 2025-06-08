import pygame

from pyui.keys import keys
from pyui.helpers import Size, Position, Mouse
from pyui.messaging import message_bus, MessageType


FRAMES_PER_SECOND = 30


def pyui_init():
    if not pygame.get_init():
        pygame.init()


class ModalState:
    def __init__(self, widget, capture):
        self.widget = widget
        self.capture = capture


class Window:
    """
    A window class that manages multiple widgets.
    The window handles initialization, rendering, and the main event loop.
    Widgets are rendered in the order they were added (first to last).
    """
    def __init__(self, size: Size, child=None, title: str = "PyUI Window"):
        pyui_init()
        self.size = size
        self.widgets = []
        self.running = False
        self.background = None
        self.mouse = Mouse()
        self.modal_backgrounds = []
        self.title = title
        
        current_surface = pygame.display.get_surface()
        if current_surface is not None:
            # If a surface already exists, we assume pygame is already initialized
            self.screen = current_surface
        else:
            self.screen = pygame.display.set_mode(self.size.as_tuple)
        if child is not None:
            self.add_widget(child)

        # define the callbacks
        message_bus.subscribe(self, MessageType.ADD_WIDGET,
                              lambda message: self.add_widget(message.data))
        message_bus.subscribe(self, MessageType.REMOVE_MODAL,
                              lambda message: self.remove_modal())

    @classmethod
    def default(cls):
        """Create a default window with a size of 800x600."""
        return cls(Size(200, 200), title="Test Window")

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.set_active(True)
        widget.parent = self
        if widget.modal:
            self.capture_background(widget)
    
    def capture_background(self, widget):
        capture = pygame.Surface(self.size.as_tuple).convert_alpha()
        capture.fill(self.background)
        # capture the current screen content
        capture.blit(self.screen, (0, 0))
        self.modal_backgrounds.append(ModalState(widget, capture))

    def remove_widget(self, widget):
        if widget in self.widgets:
            # remove if a modal background exists
            for i in self.modal_backgrounds:
                if i.widget == widget:
                    self.modal_backgrounds.remove(i)
                    break
            self.widgets.remove(widget)
            widget.parent = None

    def remove_modal(self):
        # remove the last modal widget
        if not self.widgets[-1].modal:
            # no modal widget to remove
            return
        self.widgets.pop()
        # remove the last captured background
        if self.modal_backgrounds:
            self.modal_backgrounds.pop()

    def clear_widgets(self):
        for widget in self.widgets:
            widget.parent = None
        self.widgets = []
        self.modal_backgrounds = []

    def draw(self) -> None:
        """Clear the screen and draw all widgets in order."""
        # is there a new modal widget?
        if len(self.modal_backgrounds) > 0:
            # draw the last captured background
            self.screen.blit(self.modal_backgrounds[-1].capture, (0, 0))
            # only the top widget needs to be handled
            self.widgets[-1].render(self.mouse, self.screen, Position(0, 0), self.size)
        else:
            for widget in self.widgets:
                widget.render(self.mouse, self.screen, Position(0, 0), self.size)
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        # Update mouse state
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        self.mouse.update(mouse_pos, mouse_buttons)
        
        keys_pressed = []
        keys_released = []

        for event in pygame.event.get():
            match event.type:
                case pygame.KEYDOWN:
                    keys_pressed.append(event.key)
                case pygame.KEYUP:
                    keys_released.append(event.key)
            if event.type == pygame.QUIT:
                return False
        
        keys.update(keys_pressed, keys_released)
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
            message_bus.consume()
            # Control frame rate
            pygame.time.Clock().tick(FRAMES_PER_SECOND)
        pygame.quit()
