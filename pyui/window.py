import pygame

from pyui.helpers import Size, Position


def pyui_init():
    pygame.init()


class Window:
    """
    A basic window class that manages a single widget (typically a container).
    The window handles initialization, rendering, and the main event loop.
    """
    def __init__(self, size: Size, background=(200, 200, 200), title: str = "PyUI Window"):
        pyui_init()
        self.title = title
        self.size = size
        self.child = None
        self.running = False
        self.background = background
        
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.size.as_tuple)
   
    def add_child(self, child):
        self.child = child
        self.child.parent = self

    def draw(self) -> None:
        """Clear the screen and draw the root widget."""
        self.screen.fill(self.background)
        if self.child:
            self.child.render(self.screen, Position(0, 0), self.size)
        pygame.display.flip()
    
    def handle_events(self) -> bool:
        # return False if we need to quit
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
        
        # Main loop
        self.draw()
        while self.running:
            # Handle events
            self.running = self.handle_events()
            # Control frame rate (60 FPS)
            pygame.time.Clock().tick(60)
        pygame.quit()
