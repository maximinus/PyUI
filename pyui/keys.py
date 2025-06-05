import pygame


class Key:
    # map the pygame keys to a more readable format
    ESCAPE = pygame.K_ESCAPE
    ENTER = pygame.K_RETURN


# we need to record things, or at least find them out
# was a key just pressed? Was it just released?

class KeyState:
    def __init__(self):
        self.pressed = []
        self.released = []
        self.mods = pygame.KMOD_NONE

    def update(self, pressed, released):
        self.pressed = pressed
        self.released = released
        self.mods = pygame.key.get_mods()
    
    def is_pressed(self, key):
        return key in self.pressed
    
    def is_released(self, key):
        return key in self.released

    @property
    def shift(self):
        """Check if any shift key is pressed."""
        return bool(self.mods & pygame.KMOD_SHIFT)
    
    @property
    def ctrl(self):
        """Check if any control key is pressed."""
        return bool(self.mods & pygame.KMOD_CTRL)

    @property
    def alt(self):
        """Check if any alt key is pressed."""
        return bool(self.mods & pygame.KMOD_ALT)


keys = KeyState()
