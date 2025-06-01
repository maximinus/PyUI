import unittest
from unittest.mock import Mock, patch
import pygame

from pyui.test_helper import PyuiTest
from pyui.widget import Widget
from pyui.widgets.containers import Container, HBox, VBox
from pyui.widgets.color_rect import ColorRect
from pyui.widgets.label import Label
from pyui.window import Window
from pyui.helpers import Size, Position, Margin, Expand, Align
from pyui.messaging import message_bus, MessageType, Message
from pyui.assets import get_font


class TestWidgetActive(PyuiTest):
    """Tests for the widget active flag functionality."""
    
    def setUp(self):
        super().setUp()
        # Create a clean message bus for each test
        self.original_message_bus = message_bus
        self.message_bus_patcher = patch('pyui.widget.message_bus')
        self.mock_message_bus = self.message_bus_patcher.start()
        
        # Create a widget for testing
        self.widget = Widget()
        
    def tearDown(self):
        self.message_bus_patcher.stop()
        
    def test_widget_default_inactive(self):
        """Test that widgets are inactive by default."""
        widget = Widget()
        self.assertFalse(widget.active)
        
    def test_set_active_true(self):
        """Test setting a widget to active."""
        self.widget.set_active(True)
        self.assertTrue(self.widget.active)
        
    def test_set_active_false(self):
        """Test setting a widget to inactive."""
        self.widget.active = True
        self.widget.set_active(False)
        self.assertFalse(self.widget.active)
        
    def test_set_active_remains_inactive(self):
        """Test that inactive widgets remain inactive when set_active is called with False."""
        self.widget.active = False
        self.widget.set_active(False)
        self.assertFalse(self.widget.active)


class TestContainerActive(PyuiTest):
    """Tests for the container active flag functionality."""
    
    def setUp(self):
        super().setUp()
        # Create a clean container for each test
        self.container = Container()
        self.child1 = Widget()
        self.child2 = Widget()
        
    def test_container_default_inactive(self):
        """Test that containers are inactive by default."""
        container = Container()
        self.assertFalse(container.active)
        
    def test_add_child_propagates_active_state_true(self):
        """Test that adding a child to an active container makes the child active."""
        self.container.set_active(True)
        self.container.add_child(self.child1)
        self.assertTrue(self.child1.active)
        
    def test_add_child_propagates_active_state_false(self):
        """Test that adding a child to an inactive container keeps the child inactive."""
        self.container.set_active(False)
        self.container.add_child(self.child1)
        self.assertFalse(self.child1.active)
        
    def test_set_active_propagates_to_children(self):
        """Test that setting a container to active makes all its children active."""
        self.container.add_child(self.child1)
        self.container.add_child(self.child2)
        self.container.set_active(True)
        self.assertTrue(self.child1.active)
        self.assertTrue(self.child2.active)
        
    def test_set_inactive_propagates_to_children(self):
        """Test that setting a container to inactive makes all its children inactive."""
        self.container.add_child(self.child1)
        self.container.add_child(self.child2)
        self.container.set_active(True)
        self.container.set_active(False)
        self.assertFalse(self.child1.active)
        self.assertFalse(self.child2.active)
        
    def test_remove_child_sets_inactive(self):
        """Test that removing a child from a container sets the child to inactive."""
        self.container.add_child(self.child1)
        self.container.set_active(True)
        self.assertTrue(self.child1.active)
        self.container.remove_child(self.child1)
        self.assertFalse(self.child1.active)


class TestNestedContainersActive(PyuiTest):
    """Tests for active flag propagation in nested containers."""
    
    def setUp(self):
        super().setUp()
        # Create a nested container structure for testing
        self.parent_container = Container()
        self.child_container = Container()
        self.grandchild = Widget()
        
        self.child_container.add_child(self.grandchild)
        self.parent_container.add_child(self.child_container)
        
    def test_active_propagates_to_nested_children(self):
        """Test that setting a parent container to active propagates to all nested children."""
        self.parent_container.set_active(True)
        self.assertTrue(self.parent_container.active)
        self.assertTrue(self.child_container.active)
        self.assertTrue(self.grandchild.active)
        
    def test_inactive_propagates_to_nested_children(self):
        """Test that setting a parent container to inactive propagates to all nested children."""
        self.parent_container.set_active(True)
        self.parent_container.set_active(False)
        self.assertFalse(self.parent_container.active)
        self.assertFalse(self.child_container.active)
        self.assertFalse(self.grandchild.active)


class TestHBoxVBoxActive(PyuiTest):
    """Tests for active flag functionality in HBox and VBox containers."""
    
    def setUp(self):
        super().setUp()
        # Create containers for testing
        self.hbox = HBox()
        self.vbox = VBox()
        self.widget1 = Widget()
        self.widget2 = Widget()
        
    def test_hbox_propagates_active_to_children(self):
        """Test that HBox properly propagates active state to children."""
        self.hbox.add_child(self.widget1)
        self.hbox.add_child(self.widget2)
        self.hbox.set_active(True)
        self.assertTrue(self.widget1.active)
        self.assertTrue(self.widget2.active)
        
    def test_vbox_propagates_active_to_children(self):
        """Test that VBox properly propagates active state to children."""
        self.vbox.add_child(self.widget1)
        self.vbox.add_child(self.widget2)
        self.vbox.set_active(True)
        self.assertTrue(self.widget1.active)
        self.assertTrue(self.widget2.active)


class TestWindowActive(PyuiTest):
    """Tests for active flag functionality when adding widgets to a window."""
    
    def setUp(self):
        super().setUp()
        self.window = Window(Size(100, 100))
        self.widget = Widget()
        self.container = Container()
        self.child = Widget()
        self.container.add_child(self.child)
        
    def tearDown(self):
        self.window.clear_widgets()
        
    def test_window_sets_widget_active(self):
        """Test that adding a widget to a window sets it to active."""
        self.window.add_widget(self.widget)
        self.assertTrue(self.widget.active)
        
    def test_window_sets_container_and_children_active(self):
        """Test that adding a container to a window sets it and its children to active."""
        self.window.add_widget(self.container)
        self.assertTrue(self.container.active)
        self.assertTrue(self.child.active)
        
    def test_removing_widget_from_window(self):
        """Test that removing a widget from a window doesn't automatically deactivate it."""
        # Note: Current implementation doesn't set widgets inactive when removed
        # This test documents the current behavior
        self.window.add_widget(self.widget)
        self.assertTrue(self.widget.active)
        self.window.remove_widget(self.widget)
        self.assertTrue(self.widget.active)  # Widget remains active after removal
        
    def test_clear_widgets(self):
        """Test that clearing widgets from a window doesn't deactivate them."""
        # Note: Current implementation doesn't set widgets inactive when cleared
        # This test documents the current behavior
        self.window.add_widget(self.widget)
        self.assertTrue(self.widget.active)
        self.window.clear_widgets()
        self.assertTrue(self.widget.active)  # Widget remains active after clearing


class TestMessageBlockingWithActive(unittest.TestCase):
    """Tests for message blocking based on the active flag."""
    
    def setUp(self):
        # Create a clean test environment
        self.sender = Mock()
        self.sender.active = False
        self.receiver = Mock()
        self.callback = self.receiver.callback
        self.msg_type = MessageType.ADD_WIDGET
        
        # Use the real message bus but with a clean state
        # This avoids issues with the global message bus having subscriptions
        message_bus.subscribers = {}
        message_bus.subscribed_objects = {}
        message_bus.posts = []
        
        # Subscribe the receiver
        message_bus.subscribe(self.receiver, self.msg_type, self.callback)
        
    def test_inactive_sender_messages_blocked(self):
        """Test that messages from inactive senders are blocked."""
        self.sender.active = False
        message = Message(self.msg_type, self.sender)
        message_bus.post(message)
        message_bus.consume()
        
        # Check that the callback was not called
        self.callback.assert_not_called()
        
    def test_active_sender_messages_delivered(self):
        """Test that messages from active senders are delivered."""
        self.sender.active = True
        message = Message(self.msg_type, self.sender)
        message_bus.post(message)
        message_bus.consume()
        
        # Check that the callback was called
        self.callback.assert_called_once_with(message)
        
    def test_sender_becomes_active(self):
        """Test that a sender that becomes active can send messages."""
        # First message is blocked
        self.sender.active = False
        message1 = Message(self.msg_type, self.sender)
        message_bus.post(message1)
        message_bus.consume()
        self.callback.assert_not_called()
        
        # Sender becomes active, second message is delivered
        self.sender.active = True
        message2 = Message(self.msg_type, self.sender)
        message_bus.post(message2)
        message_bus.consume()
        self.callback.assert_called_once_with(message2)
        
    def test_sender_becomes_inactive(self):
        """Test that a sender that becomes inactive has messages blocked."""
        # First message is delivered
        self.sender.active = True
        message1 = Message(self.msg_type, self.sender)
        message_bus.post(message1)
        message_bus.consume()
        self.callback.assert_called_once_with(message1)
        
        # Reset mock
        self.callback.reset_mock()
        
        # Sender becomes inactive, second message is blocked
        self.sender.active = False
        message2 = Message(self.msg_type, self.sender)
        message_bus.post(message2)
        message_bus.consume()
        self.callback.assert_not_called()


class TestIntegrationActiveWithComponents(PyuiTest):
    """Integration tests for active flag with actual UI components."""
    
    def setUp(self):
        super().setUp()
        self.window = Window(Size(200, 200))
        
        # Create a test font
        self.font = get_font("creato.otf", 16)
        
        # Create widgets for testing
        self.color_rect = ColorRect((255, 0, 0), Size(50, 50))
        self.label = Label("Test", self.font)
        
        # Create containers
        self.hbox = HBox()
        self.hbox.add_child(self.color_rect)
        self.hbox.add_child(self.label)
    
    def tearDown(self):
        self.window.clear_widgets()
    
    def test_integration_window_container_components(self):
        """Test that adding components to a window through containers works with active flag."""
        # Initially all widgets are inactive
        self.assertFalse(self.hbox.active)
        self.assertFalse(self.color_rect.active)
        self.assertFalse(self.label.active)
        
        # Adding container to window activates everything
        self.window.add_widget(self.hbox)
        self.assertTrue(self.hbox.active)
        self.assertTrue(self.color_rect.active)
        self.assertTrue(self.label.active)
        
        # Create and add a new widget to the container
        new_label = Label("New", self.font)
        self.assertFalse(new_label.active)
        self.hbox.add_child(new_label)
        self.assertTrue(new_label.active)
        
        # Remove a widget from the container
        self.hbox.remove_child(self.color_rect)
        self.assertFalse(self.color_rect.active)


if __name__ == "__main__":
    unittest.main()
