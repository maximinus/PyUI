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
        if widget is None:
            return
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
        self.frame_events = []
        self.dirty_widgets = []

    def push_frame(self, frame):
        # when push and pop are done like this, so we can iterate from newest to oldest
        callbacks = get_ordered_callbacks(frame)
        self.frame_events.insert(0, FrameEvents(frame, callbacks))

    def pop_frame(self):
        if len(self.frame_events) > 0:
            self.frame_events.pop(0)

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
            self.update_dirty_widgets()
            clock.tick(60)

    def draw_all_frames(self):
        for frame in self.frame_events:
            frame.frame.render(self.display, None, DEFAULT_SIZE)
        pygame.display.flip()

    def handle_event(self, event):
        # cycle through the frames
        for frame in self.frame_events:
            for handler in frame.get_handlers(event.type):
                if handler.callback(event):
                    # event has been dealt with
                    return

    def set_dirty(self, widget):
        # store a widget that needs to be updated
        # the widget should know what to do to update itself
        self.dirty_widgets.append(widget)

    def update_dirty_widgets(self):
        # go through all dirty rects and sort by frame (we draw from back to front)
        frame_rects = {}
        for widget in self.dirty_widgets:
            parent = widget.get_root()
            if parent in frame_rects:
                frame_rects[parent].append(widget)
            else:
                frame_rects[parent] = [widget]
        # loop through frames looking for a match
        for frame_event in reversed(self.frame_events):
            if frame_event.frame in frame_rects:
                # update all the widgets that are dirty in this frame
                for widget in frame_rects[frame_event.frame]:
                    widget.update(self.display)
            # TODO: Since we render from the back to the front, a widget may overwrite a frame in front
            # because of this, we need a routine that checks for overlaps and then redraws any
            # parts of the frames that are in front of the one that was updated
        pygame.display.flip()


app = PyUIApp()
