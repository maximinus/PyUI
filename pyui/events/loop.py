import sys
import pygame

from pyui.setup import init, get_clock, DEFAULT_SIZE
from pyui.theme import THEME
from pyui.events.events import PyUiEvent, is_mouse_click, Event

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
    def __init__(self, callback, event_type, widget):
        self.callback = callback
        self.event_type = event_type
        self.widget = widget


class FrameEvents:
    # all the frames have a list of events as well
    def __init__(self, frame, callbacks=None):
        self.frame = frame
        if callbacks is None:
            self.callbacks = []
        else:
            self.callbacks = callbacks

    def get_filtered_callbacks(self, event_type):
        # go through list in reverse
        # we are looking for events that catch these events
        all_callbacks = []
        for callback in reversed(self.callbacks):
            if callback.event_type == event_type:
                all_callbacks.append(callback)
            # another possibility is the check for a "noclick" event type
            if is_mouse_click(event_type) and callback.event_type == Event.ClickOutside:
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
        self.looping = False
        self.deferred_frames = []
        self.dead_frames = []

    def push_frame(self, frame):
        # push and pop are done like this to iterate from newest to oldest
        if not self.looping:
            self.add_frame(frame)
        else:
            # we cannot add a frame during a loop, it must be after
            self.deferred_frames.append(frame)

    def add_frame(self, frame):
        callbacks = get_ordered_callbacks(frame)
        self.frame_events.insert(0, FrameEvents(frame, callbacks))

    def pop_frame(self):
        # TODO: shouldn't destroy a frame during a loop either
        if len(self.frame_events) > 0:
            self.frame_events.pop(0)

    def remove_frame(self, frame):
        self.dead_frames.append(frame)

    def event_loop(self):
        self.display.fill(THEME.color['widget_background'])
        self.draw_all_frames()
        clock = get_clock()
        self.looping = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(True)
                pyui_event = PyUiEvent.event(event)
                if pyui_event is not None:
                    self.handle_event(pyui_event)
            self.update_dirty_widgets()
            self.remove_dead_frames()
            self.add_deferred_frames()
            clock.tick(60)

    def remove_dead_frames(self):
        # remove the frame. This means we need to update the dirty frames
        pass

    def add_deferred_frames(self):
        if len(self.deferred_frames) == 0:
            return
        for frame in self.deferred_frames:
            # add the frame, and draw it
            self.add_frame(frame)
            self.frame_events[0].frame.render(self.display, None, DEFAULT_SIZE)
        pygame.display.flip()
        self.deferred_frames = []

    def draw_all_frames(self):
        for frame in self.frame_events:
            frame.frame.render(self.display, None, DEFAULT_SIZE)
        pygame.display.flip()

    def handle_event(self, event):
        # cycle through the frames
        # do it this way in case something adds a handler in an event
        for frame in self.frame_events:
            for callback in [y for y in frame.get_filtered_callbacks(event.type)]:
                # if it is a mouse click, we need to validate the widgets render_rect against this clock position
                if is_mouse_click(event.type):
                    if callback.widget.render_rect is None:
                        # not yet rendered, so cannot get a click, ignore this one
                        continue
                    # some widgets need to know if a click was NOT made in their widget
                    # ensure the click was in the widget
                    if not callback.widget.render_rect.collidepoint(event.xpos, event.ypos):
                        # didn't click this widget, so maybe ignore
                        if callback.event_type != Event.ClickOutside:
                            continue
                if callback.callback(event):
                    # event has been dealt with
                    return
            if frame.frame.modal:
                # ignore all other frames past this one
                return

    def set_dirty(self, widget):
        # store a widget that needs to be updated
        # the widget should know what to do to update itself
        self.dirty_widgets.append(widget)

    def update_dirty_widgets(self):
        # go through all dirty rects and sort by frame (we draw from back to front)
        if len(self.dirty_widgets) == 0:
            # nothing to update
            return
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
        # finally, clear all list or dirty widgets
        self.dirty_widgets = []


app = PyUIApp()
