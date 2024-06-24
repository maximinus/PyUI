import sys

import pygame


# When a widget is created, it can ask for events or not
# When a SDL event happens, we first of all look at what widget is covering that screen
# In every PyUi app, each window consists of exactly one widget
# We drill down that widget to ask if it needs this event
# If it doesn't, we then drill UP to the widgets parent to see if it needs that event
# A widget can block events from rising up the menu

# Things can send events, it's not just the SDL events that cause this
# As a GUI, we only look at key presses and mouse clicks for now

# No need to rewrite events classes, use the SDL ones

class PyUIApp:
    def __init__(self, frame=None):
        if frame is None:
            self.frames = []
        else:
            self.frames = [frame]

    def push_frame(self, frame):
        # when push and pop are done like this, we can iterate from
        # newest to oldest
        self.frames.insert(0, frame)

    def pop_frame(self):
        if len(self.frames) > 0:
            self.frames.pop(0)

    def event_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(True)
                self.handle_event(event)
                clock.tick(60)

    def handle_event(self, event):
        # get the event and pass to the top window
        # if not consumed, then it goes to the next, and so on
        # the parent of the widget is the one that will know if the event can
        # be processed or not; and every widget needs a parent frame or border
        # It's not as simple as that entirely though; a widget might need to know
        # if the mouse is outside the widget in question

        # for now, only handle mouse events
        if event.type != pygame.MOUSEMOTION:
            return
        for frame in self.frames:
            frame.handle_event(event)
