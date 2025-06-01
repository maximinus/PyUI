import unittest
from unittest.mock import Mock

from pyui.messaging import MessageType, Message, MessageBus, message_bus


class TestMessage(unittest.TestCase):
    def test_message_initialization(self):
        """Test that a Message is correctly initialized with its properties."""
        msg_type = MessageType.ADD_WIDGET
        sender = "test_sender"
        data = {"key": "value"}
        
        message = Message(msg_type, sender, data)
        
        self.assertEqual(message.type, msg_type)
        self.assertEqual(message.sender, sender)
        self.assertEqual(message.data, data)
    
    def test_message_initialization_without_data(self):
        """Test that a Message can be initialized without data."""
        msg_type = MessageType.ADD_WIDGET
        sender = "test_sender"
        
        message = Message(msg_type, sender)
        self.assertEqual(message.type, msg_type)
        self.assertEqual(message.sender, sender)
        self.assertIsNone(message.data)


class TestMessageBus(unittest.TestCase):
    """Tests for the MessageBus class."""
    
    def setUp(self):
        """Set up a fresh MessageBus for each test."""
        self.bus = MessageBus()
    
    def test_subscribe(self):
        """Test that a subscriber can subscribe to a message type."""
        subscriber = "test_subscriber"
        msg_type = MessageType.ADD_WIDGET
        callback = Mock()
        
        self.bus.subscribe(subscriber, msg_type, callback)
        
        self.assertIn(msg_type, self.bus.subscribers)
        self.assertIn(callback, self.bus.subscribers[msg_type])
        self.assertIn(subscriber, self.bus.subscribed_objects)
        self.assertIn(msg_type, self.bus.subscribed_objects[subscriber])
    
    def test_unsubscribe_specific_type(self):
        """Test that a subscriber can unsubscribe from a specific message type."""
        class TestSubscriber:
            def callback(self, message):
                pass
        
        subscriber = TestSubscriber()
        msg_type = MessageType.ADD_WIDGET
        
        self.bus.subscribe(subscriber, msg_type, subscriber.callback)
        self.bus.unsubscribe(subscriber, msg_type)
        
        # Check that the subscriber is no longer subscribed to the message type
        self.assertNotIn(subscriber, self.bus.subscribed_objects)
        # If there are no subscribers for a message type, the key is removed
        self.assertNotIn(msg_type, self.bus.subscribers)
    
    def test_unsubscribe_all(self):
        """Test that a subscriber can unsubscribe from all message types."""
        subscriber = Mock()
        msg_type1 = MessageType.ADD_WIDGET
        msg_type2 = MessageType.ADD_WIDGET
        callback1 = subscriber.callback1
        callback2 = subscriber.callback2
        
        self.bus.subscribe(subscriber, msg_type1, callback1)
        self.bus.subscribe(subscriber, msg_type2, callback2)
        self.bus.unsubscribe(subscriber)
        
        # Check that the subscriber is completely unsubscribed
        self.assertNotIn(subscriber, self.bus.subscribed_objects)
    
    def test_post_message(self):
        """Test that posting a message calls the appropriate callbacks."""
        subscriber = Mock()
        msg_type = MessageType.ADD_WIDGET
        callback = subscriber.callback
        
        self.bus.subscribe(subscriber, msg_type, callback)
        message = Message(msg_type, subscriber)
        self.bus.post(message)
        self.bus.consume()
        
        # Check that the callback was called with the message
        subscriber.callback.assert_called_once_with(message)

    def test_post_message_no_consume(self):
        """Test that posting a message does not call anything"""
        subscriber = Mock()
        msg_type = MessageType.ADD_WIDGET
        callback = subscriber.callback
        
        self.bus.subscribe(subscriber, msg_type, callback)
        message = Message(msg_type, "sender")
        self.bus.post(message)
        
        # Check that the callback was called with the message
        subscriber.callback.assert_not_called()

    def test_post_message_multiple_subscribers(self):
        """Test that posting a message calls multiple subscribers."""
        subscriber1 = Mock()
        subscriber2 = Mock()
        msg_type = MessageType.ADD_WIDGET
        
        self.bus.subscribe(subscriber1, msg_type, subscriber1.callback)
        self.bus.subscribe(subscriber2, msg_type, subscriber2.callback)
        message = Message(msg_type, subscriber1)
        self.bus.post(message)
        self.bus.consume()
        
        # Check that both callbacks were called with the message
        subscriber1.callback.assert_called_once_with(message)
        subscriber2.callback.assert_called_once_with(message)
    
    def test_post_message_no_subscribers(self):
        """Test that posting a message with no subscribers doesn't error."""
        msg_type = MessageType.ADD_WIDGET
        message = Message(msg_type, "sender")
        
        # This should not raise an exception
        self.bus.post(message)
