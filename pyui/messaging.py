from typing import Dict, List, Any, Callable, Set
from enum import Enum, auto


class MessageType(Enum):
    """Common message types that can be used throughout the application."""
    ADD_WIDGET = auto()


class Message:
    """A message that can be sent through the messaging system."""
    def __init__(self, msg_type: MessageType, sender: Any, data: Any = None):
        self.type = msg_type
        self.sender = sender
        self.data = data


class MessageBus:
    """Central messaging system that routes messages between components."""
    def __init__(self):
        self.subscribers: Dict[MessageType, List[Callable[[Message], None]]] = {}
        self.subscribed_objects: Dict[Any, Set[MessageType]] = {}
    
    def subscribe(self, subscriber: Any, msg_type: MessageType, callback: Callable[[Message], None]) -> None:
        """Subscribe to a specific message type with a callback function."""
        if msg_type not in self.subscribers:
            self.subscribers[msg_type] = []
        
        self.subscribers[msg_type].append(callback)
        
        if subscriber not in self.subscribed_objects:
            self.subscribed_objects[subscriber] = set()
        
        self.subscribed_objects[subscriber].add(msg_type)
    
    def unsubscribe(self, subscriber: Any, msg_type: MessageType = None) -> None:
        """
        Unsubscribe from messages.
        If msg_type is None, unsubscribe from all message types.
        """
        if subscriber not in self.subscribed_objects:
            return
        
        if msg_type is None:
            # Unsubscribe from all message types
            for mt in list(self.subscribed_objects[subscriber]):
                self.unsubscribe_from_type(subscriber, mt)
            del self.subscribed_objects[subscriber]
        else:
            # Unsubscribe from specific message type
            self.unsubscribe_from_type(subscriber, msg_type)
            self.subscribed_objects[subscriber].discard(msg_type)
            if not self.subscribed_objects[subscriber]:
                del self.subscribed_objects[subscriber]
    
    def unsubscribe_from_type(self, subscriber: Any, msg_type: MessageType) -> None:
        """Helper method to unsubscribe an object from a specific message type."""
        if msg_type not in self.subscribers:
            return
        
        # Create a new list without the subscriber's callbacks
        self.subscribers[msg_type] = [
            cb for cb in self.subscribers[msg_type]
            if getattr(cb, '__self__', None) is not subscriber
        ]
        
        if not self.subscribers[msg_type]:
            del self.subscribers[msg_type]
    
    def post(self, message: Message) -> None:
        """Post a message to all subscribers of that message type."""
        if message.type not in self.subscribers:
            return
        
        for callback in self.subscribers[message.type]:
            callback(message)


# Singleton instance that can be imported
message_bus = MessageBus()
