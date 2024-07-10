# There are 2 types of events

# SDL events and system events
# They should be treated in the exact same way


class EventQueue:
    def __init__(self):
        self.event_listeners = {}
        self.events = []

    def add_listener(self, event_type, callback):
        if event_type in self.event_listeners:
            self.event_listeners[event_type].append(callback)
        else:
            self.event_listeners[event_type] = [callback]

    def process_event(self, event):
        if event.type not in self.event_listeners:
            return False
        # if a callback returns True, we finish this event
        for callback in self.event_listeners[event.type]:
            if callback(event):
                return True
        return False


ev_queue = EventQueue()


def add_listener(event_type, callback):
    ev_queue.add_listener(event_type, callback)


def add_event(event):
    ev_queue.events.append(event)
