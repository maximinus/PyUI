import sys

import pygame

from pyui.base import Position
from pyui.events.events import PyUiEvent, Event


# SDL events and system events
# They should be treated in the exact same way

def filter_out_mouse_moves(events):
    # we are only interested in the LAST mouse move event in every frame, so remove the rest
    mouse_move_found = False
    filtered_events = []
    for event in reversed(events):
        if event.type == Event.MouseMove:
            if not mouse_move_found:
                filtered_events.append(event)
                mouse_move_found = True
        else:
            filtered_events.append(event)
    filtered_events.reverse()
    return filtered_events


class Callback:
    # function is the actual callback
    # Widget is the widget (or None if not widget based)
    # data is passed along to the function, which must accept 2 arguments
    def __init__(self, function, widget=None, func_arg=None):
        self.function = function
        self.widget = widget
        self.frame = None
        if self.widget is not None:
            self.frame = self.widget.parent
        self.func_arg = func_arg

    def call_function(self, event):
        self.function(event, self.func_arg)


class SortedCallbacks:
    # to handle sorting by frame, we hold all the callbacks to an event by frame and by "others"
    def __init__(self):
        self.frame_events = {}
        self.others = []

    def add(self, callback):
        if callback.frame is None:
            self.others.append(callback)
        if callback.frame in self.frame_events:
            self.frame_events[callback.frame].append(callback)
        else:
            self.frame_events[callback.frame] = [callback]

    def remove_frame(self, frame):
        if frame in self.frame_events:
            del self.frame_events[frame]


class EventQueue:
    def __init__(self):
        self.event_listeners = {}
        # these are the events raised by PyUI code
        # they are cleared and acted on each frame
        self.events = []

    def add_listener(self, event_type, callback):
        if event_type in self.event_listeners:
            self.event_listeners[event_type].append(callback)
        else:
            self.event_listeners[event_type] = SortedCallbacks()
            self.event_listeners[event_type].add(callback)

    def filter_events(self, event_types):
        # get all these event types, event_types may be a list, or maybe not
        if type(event_types) is list:
            listeners = []
            for et in event_types:
                if et in self.event_listeners:
                    listeners.extend(self.event_listeners[et])
            return listeners
        else:
            if event_types in self.event_listeners:
                return self.event_listeners[event_types]
        return []

    def process_all_events(self):
        # convert all pygame events into our events
        pyui_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(True)
            pyui_event = PyUiEvent.event(event)
            if pyui_event is not None:
                pyui_events.append(pyui_event)

        pyui_events = filter_out_mouse_moves(pyui_events)
        pyui_events.extend(self.events)
        self.events = []
        for single_event in pyui_events:
            self.process_single_event(single_event)

    def process_single_event(self, event):
        if event.type == Event.MouseMove:
            self.handle_mouse_move_event(event)
            return

        if event.type not in self.event_listeners:
            return False
        # if a callback returns True, we finish this event
        for callback in self.event_listeners[event.type]:
            if callback(event):
                return True
        return False

    def handle_mouse_move_event(self, event):
        # get the widgets looking for the events MouseIn, MouseOut, MouseMove
        # we need check these in frame order, as a frame may be modal
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
                if callback.widget.mouse_hit(mouse_pos):
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


ev_queue = EventQueue()


def add_listener(event_type, callback):
    ev_queue.add_listener(event_type, callback)


def add_event(event):
    ev_queue.events.append(event)
