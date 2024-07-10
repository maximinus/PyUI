import sys
import pygame

from pyui.base import Position
from pyui.setup import init, get_clock, DEFAULT_SIZE
from pyui.theme import THEME
from pyui.events.events import PyUiEvent, is_mouse_click, Event, adjust_mouse_coords, FrameClosed

BACKGROUND_COLOR = (140, 140, 140)

# When a widget is created, it has a list of [event_type, callback] structures
# When a SDL event happens, we first of all look at what frames are on the screen
# In every PyUi app, each window consists of exactly one widget
# We drill down that widget to ask if it needs this event
# If it doesn't, we then drill UP to the widgets parent to see if it needs that event
# A widget can block events from rising up the menu, but not down
# Although it appears simple, there are issues:

# We like clean code that states our intentions, so we use "Clicked" and also test against a widgets position
# But then sometimes we want to catch the event "Not clicked" - an event that could be consumed by something else!
# perhaps we can add the idea of FOCUS
# this means a widget can have extra callbacks that are only used when it has focus
# One of those callbacks is "not clicked here". Is that the only event we would want?
# Only the widget with focus gets keyboard input???
# 2 widgets can have focus, they would be sent the same messages

# Edit: Event should signal intent, if extra code is required here thats fine

# Things can send events, it's not just the SDL events that cause this
# When things are done, we also raise an event
# As a GUI, we only look at key presses and mouse clicks for now


class CallbackData:
    def __init__(self, event, data):
        self.event = event
        self.data = data

    def __repr__(self):
        return f'CallbackData: {self.event}, {self.data}'


class Callback:
    def __init__(self, callback, event_type, widget, data=None):
        self.callback = callback
        self.event_type = event_type
        self.widget = widget
        # data is custom per event, although not used for SDL events
        self.data = data

    def __repr__(self):
        return f'Callback: {self.event_type}, {self.callback}'


class FrameEvents:
    # all the frames have a list of events as well
    def __init__(self, frame, callbacks=None):
        self.frame = frame
        if callbacks is None:
            self.callbacks = []
        else:
            self.callbacks = callbacks

    def get_filtered_callbacks(self, event_types):
        # go through list in reverse
        # we are looking for events that catch these events
        all_callbacks = []
        for callback in reversed(self.callbacks):
            if callback.event_type in event_types:
                all_callbacks.append(callback)
        return all_callbacks


def get_ordered_callbacks(frame):
    # get the children by depth first search
    all_widgets = []

    def depth_first_search(widget):
        if widget is None:
            return
        if widget.container:
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
        self.window_data = []
        self.dirty_widgets = []
        self.looping = False
        self.deferred_frames = []
        self.dead_frames = []
        # things that happened this screen frame
        # these are acted on in the next frame
        self.frame_events = []
        self.widgets_overlapped = []

    def reset(self):
        # used in tests and debugging
        self.window_data = []
        self.dirty_widgets = []
        self.looping = False
        self.deferred_frames = []
        self.dead_frames = []
        self.frame_events = []

    def push_frame(self, frame):
        # push and pop are done like this to iterate from newest to oldest
        if not self.looping:
            self.add_frame(frame)
        else:
            # we cannot add a frame during a loop, it must be after
            self.deferred_frames.append(frame)

    def add_frame(self, frame):
        callbacks = get_ordered_callbacks(frame)
        self.window_data.insert(0, FrameEvents(frame, callbacks))

    def pop_frame(self):
        # TODO: shouldn't destroy a frame during a loop either
        if len(self.window_data) > 0:
            self.window_data.pop(0)

    def remove_frame(self, frame):
        self.dead_frames.append(frame)

    def event_loop(self):
        self.draw_all_frames()
        clock = get_clock()
        self.looping = True
        while True:
            # convert all pygame events into our events
            pyui_events = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(True)
                pyui_event = PyUiEvent.event(event)
                if pyui_event is not None:
                    pyui_events.append(pyui_event)

            # we are only interested in the LAST mouse move event in every frame, so remove the rest
            mouse_move_found = False
            filtered_events = []
            for event in reversed(pyui_events):
                if event.type == Event.MouseMove:
                    if not mouse_move_found:
                        filtered_events.append(event)
                        mouse_move_found = True
                else:
                    filtered_events.append(event)
            filtered_events.reverse()
            pyui_events = filtered_events

            pyui_events.extend(self.frame_events)
            self.frame_events = []
            for single_event in pyui_events:
                self.handle_event(single_event)
            if not self.remove_dead_frames():
                self.update_dirty_widgets()
            else:
                # if a frame is deleted, all frames are rendered anyway
                self.dirty_widgets = []
            self.add_deferred_frames()
            pygame.display.flip()
            clock.tick(60)

    def remove_dead_frames(self):
        # remove the frame. This means we need to update the dirty frames
        if len(self.dead_frames) == 0:
            return
        kept_frames = []
        for window in self.window_data:
            if window.frame not in self.dead_frames:
                kept_frames.append(window)
            else:
                # this frame will be deleted, so create a new event
                self.frame_events.append(FrameClosed(frame=window.frame))
        self.window_data = kept_frames
        self.dead_frames = []
        self.draw_all_frames()

    def add_deferred_frames(self):
        if len(self.deferred_frames) == 0:
            return
        for frame in self.deferred_frames:
            # add the frame, and draw it
            self.add_frame(frame)
            self.window_data[0].frame.render(self.display, None, DEFAULT_SIZE)
        self.deferred_frames = []

    def draw_all_frames(self):
        self.display.fill(THEME.color['widget_background'])
        for window in self.window_data:
            window.frame.render(self.display, None)
            pos = window.frame.position
            self.display.blit(window.frame.texture, (pos.x, pos.y))
        pygame.display.flip()

    def handle_event(self, event):
        # cycle through the frames
        # do it this way in case something adds a handler in an event

        # some events are tied to mouse move events, so handle those differently
        # per frame there could be multiple mouse move events. However, we are only sent the last one
        if event.type == Event.MouseMove:
            self.handle_mouse_move_event(event)
            return

        for frame in self.window_data:
            # get all callbacks listening to this event
            for callback in [y for y in frame.get_filtered_callbacks([event.type])]:
                # if any kind of mouse event, then we need to offset the coords by the frames position
                event = adjust_mouse_coords(frame.frame.position, event)
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
                if callback.callback(CallbackData(event, callback.data)):
                    # event has been dealt with
                    return
            if frame.frame.modal:
                # ignore all other frames past this one
                return

    def handle_mouse_move_event(self, event):
        # get the widgets looking for the events MouseIn, MouseOut, MouseMove
        for window in self.window_data:
            frame_pos = window.frame.position
            callbacks = window.get_filtered_callbacks([Event.MouseIn, Event.MouseOut, Event.MouseMove])
            # look for events looking for EventIn
            callbacks_inside = []
            callbacks_outside = []
            # get mouse position after removing window offset
            mouse_pos = Position(event.xpos - frame_pos.x, event.ypos - frame_pos.y)
            for callback in callbacks:
                # are we in this widget?
                if callback.widget.mouse_rect.collidepoint((mouse_pos.x, mouse_pos.y)):
                    # if the widget has been handled already, ignore
                    if callback.widget not in self.widgets_overlapped:
                        if callback.event_type == Event.MouseIn:
                            callbacks_inside.append(callback)
                else:
                    if callback.event_type == Event.MouseOut:
                        # only call if it is currently inside
                        if callback.widget in self.widgets_overlapped:
                            callbacks_outside.append(callback)

            for callback in callbacks_outside:
                if callback.widget in self.widgets_overlapped:
                    # update the widget, we have moved outside
                    callback.callback(CallbackData(event, callback.data))
                    self.widgets_overlapped.remove(callback.widget)

            for callback in callbacks_inside:
                callback.callback(CallbackData(event, callback.data))
                self.widgets_overlapped.append(callback.widget)

    def set_dirty(self, widget):
        # store a widget that needs to be updated
        # the widget should have already updated itself by this point
        self.dirty_widgets.append(widget)

    def update_dirty_widgets(self):
        # the widgets have redrawn themselves, but no re-sizing has been done
        # we have the frame offset for each widget.
        # What we do is update all frames and update that area of the frame
        # first thing to do it calculate the screen rectangle to update
        if len(self.dirty_widgets) == 0:
            return

        for window in self.window_data:
            areas = []
            for widget in self.dirty_widgets:
                update = window.frame.update_dirty_widget(widget)
                # pygame rect or None
                if update is not None:
                    areas.append(update)
            frame_pos = window.frame.position
            for area in areas:
                # the area is the SCREEN position to blit to, we need to adjust slightly
                screen_pos = (area.x, area.y)
                self.display.blit(window.frame.texture, screen_pos,
                                  (area.x - frame_pos.x, area.y - frame_pos.y, area.width, area.height))
        self.dirty_widgets = []


app = PyUIApp()
