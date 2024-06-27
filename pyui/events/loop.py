import sys
import pygame

from pyui.setup import init, get_clock, DEFAULT_SIZE
from pyui.theme import THEME
from pyui.events.events import PyUiEvent

BACKGROUND_COLOR = (140, 140, 140)

# When a widget is created, it can ask for events or not
# When a SDL event happens, we first of all look at what widget is covering that screen
# In every PyUi app, each window consists of exactly one widget
# We drill down that widget to ask if it needs this event
# If it doesn't, we then drill UP to the widgets parent to see if it needs that event
# A widget can block events from rising up the menu

# Things can send events, it's not just the SDL events that cause this
# As a GUI, we only look at key presses and mouse clicks for now


class Callback:
    def __init__(self, callback, event_type):
        self.callback = callback
        self.event_type = event_type


class FrameEvents:
    # all the frames have a list of events as well
    def __init__(self, frame, callbacks=None):
        self.frame = frame
        if callbacks is None:
            self.callbacks = []
        else:
            self.callbacks = callbacks

    def get_handlers(self, event_type):
        # go through list in reverse
        all_callbacks = []
        for callback in reversed(self.callbacks):
            if callback.event_type == event_type:
                all_callbacks.append(callback)
        return all_callbacks


def get_ordered_callbacks(frame):
    # get the children by depth first search
    all_widgets = []

    def depth_first_search(widget):
        for child in widget.children:
            depth_first_search(child)
        all_widgets.append(widget)

    # iterate over list and return all callbacks
    depth_first_search(frame)
    callbacks = []
    for widget in all_widgets:
        callbacks.extend(widget.callbacks)
    return callbacks


class PyUIApp:
    def __init__(self, window_size=None):
        self.display = init(size=window_size)
        self.frames = []

    def push_frame(self, frame):
        # when push and pop are done like this, so we can iterate from newest to oldest
        callbacks = get_ordered_callbacks(frame)
        self.frames.insert(0, FrameEvents(frame, callbacks))

    def pop_frame(self):
        if len(self.frames) > 0:
            self.frames.pop(0)

    def event_loop(self):
        self.display.fill(THEME.color['widget_background'])
        self.draw_all_frames()
        clock = get_clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(True)
                pyui_event = PyUiEvent.event(event)
                if pyui_event is not None:
                    self.handle_event(pyui_event)
            clock.tick(60)

    def draw_all_frames(self):
        for frame in self.frames:
            frame.frame.render(self.display, None, DEFAULT_SIZE)
        pygame.display.flip()

    def register(self, widget, event_type, callback):
        # we are going to need to know the root frame that contains this widget
        # because that frame may be modal
        root_frame = widget.get_root()
        for frame in self.frames:
            if frame.frame == root_frame:
                frame.callbacks.append(Callback(callback, event_type))

    def handle_event(self, event):
        # cycle through the frames
        print(event)
        for frame in self.frames:
            print(frame.get_handlers(event.type))
            for handler in frame.get_handlers(event.type):
                if handler(event):
                    # event has been dealt with
                    return

    def set_dirty(self, rect):
        # tells the app what to redraw next frame
        pass


app = PyUIApp()
