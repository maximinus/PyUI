import pygame
from unittest.mock import MagicMock, patch

from pyui.test_helper import PyuiTest
from pyui.window import Window
from pyui.widget import Widget
from pyui.helpers import Size, Position


class MockWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_called = False
        self.render_position = None
        self.render_size = None
        self.update_called = False
        self.update_mouse = None
        self.update_surface = None
        self.update_pos = None
        self.update_size = None
    
    def render(self, mouse, surface, pos, size):
        self.render_called = True
        self.render_position = pos
        self.render_size = size


class TestWindow(PyuiTest):
    def setUp(self):
        # Create a small window for testing
        self.size = Size(200, 200)
        self.window = Window(self.size, title="Test Window")
    
    def tearDown(self):
        # Clean up
        self.window.running = False
        if hasattr(self.window, 'screen'):
            pygame.display.quit()
    
    def test_init(self):
        # Test initialization
        self.assertEqual(self.window.title, "Test Window")
        self.assertEqual(self.window.size, self.size)
        self.assertEqual(self.window.widgets, [])
        self.assertFalse(self.window.running)
        self.assertEqual(self.window.background, (200, 200, 200))
    
    def test_add_widget(self):
        # Test adding a widget
        widget = MockWidget()
        self.window.add_widget(widget)
        
        self.assertEqual(len(self.window.widgets), 1)
        self.assertEqual(self.window.widgets[0], widget)
        self.assertEqual(widget.parent, self.window)
    
    def test_remove_widget(self):
        # Test removing a widget
        widget1 = MockWidget()
        widget2 = MockWidget()
        
        self.window.add_widget(widget1)
        self.window.add_widget(widget2)
        self.assertEqual(len(self.window.widgets), 2)
        
        self.window.remove_widget(widget1)
        self.assertEqual(len(self.window.widgets), 1)
        self.assertEqual(self.window.widgets[0], widget2)
        self.assertIsNone(widget1.parent)
        self.assertEqual(widget2.parent, self.window)
    
    def test_clear_widgets(self):
        # Test clearing all widgets
        widget1 = MockWidget()
        widget2 = MockWidget()
        
        self.window.add_widget(widget1)
        self.window.add_widget(widget2)
        self.assertEqual(len(self.window.widgets), 2)
        
        self.window.clear_widgets()
        self.assertEqual(len(self.window.widgets), 0)
        self.assertIsNone(widget1.parent)
        self.assertIsNone(widget2.parent)
    
    def test_draw(self):
        # Test drawing widgets
        widget1 = MockWidget()
        widget2 = MockWidget()
        
        self.window.add_widget(widget1)
        self.window.add_widget(widget2)
        
        # Patch pygame.display.flip to avoid actual screen updates
        with patch('pygame.display.flip'):
            self.window.draw()
        
        # Check that both widgets were rendered
        self.assertTrue(widget1.render_called)
        self.assertTrue(widget2.render_called)
        
        # Check render parameters
        self.assertEqual(widget1.render_position, Position(0, 0))
        self.assertEqual(widget1.render_size, self.size)
        self.assertEqual(widget2.render_position, Position(0, 0))
        self.assertEqual(widget2.render_size, self.size)
    
    def test_render_order(self):
        # Test that widgets are rendered in the order they were added
        widgets = []
        render_order = []
        
        # Create a custom mock to track render order
        class OrderTrackingWidget(Widget):
            def __init__(self, index):
                super().__init__()
                self.index = index
                
            def render(self, mouse, surface, pos, size):
                render_order.append(self.index)
        
        # Add widgets
        for i in range(3):
            widget = OrderTrackingWidget(i)
            widgets.append(widget)
            self.window.add_widget(widget)
        
        # Draw the window
        with patch('pygame.display.flip'):
            self.window.draw()
        
        # Check the render order
        self.assertEqual(render_order, [0, 1, 2])
    
    def test_handle_events_quit(self):
        # Test that the window stops running when a quit event is received
        # Create a mock event
        mock_event = MagicMock()
        mock_event.type = pygame.QUIT
        
        # Patch pygame.event.get to return our mock event
        with patch('pygame.event.get', return_value=[mock_event]):
            result = self.window.handle_events()
        
        # The method should return False to indicate the window should stop running
        self.assertFalse(result)
    
    def test_handle_events_no_quit(self):
        # Test that the window continues running when no quit event is received
        # Patch pygame.event.get to return an empty list (no events)
        with patch('pygame.event.get', return_value=[]):
            result = self.window.handle_events()
        
        # The method should return True to indicate the window should continue running
        self.assertTrue(result)
        
    def test_mouse_initialization(self):
        # Test that Mouse object is properly initialized in Window
        self.assertIsNotNone(self.window.mouse)
        self.assertEqual(self.window.mouse.position.x, 0)
        self.assertEqual(self.window.mouse.position.y, 0)
        self.assertFalse(self.window.mouse.left.state)
        self.assertFalse(self.window.mouse.middle.state)
        self.assertFalse(self.window.mouse.right.state)
        
    def test_mouse_update_in_handle_events(self):
        # Test that mouse state is updated in handle_events
        mock_pos = (100, 150)
        mock_buttons = (True, False, True)
        
        # Patch pygame.mouse.get_pos and pygame.mouse.get_pressed
        with patch('pygame.mouse.get_pos', return_value=mock_pos), \
             patch('pygame.mouse.get_pressed', return_value=mock_buttons), \
             patch('pygame.event.get', return_value=[]):
            self.window.handle_events()
        
        # Check that mouse state was updated
        self.assertEqual(self.window.mouse.position.x, 100)
        self.assertEqual(self.window.mouse.position.y, 150)
        self.assertTrue(self.window.mouse.left.state)
        self.assertFalse(self.window.mouse.middle.state)
        self.assertTrue(self.window.mouse.right.state)
    
    def test_run_calls_handle_events_and_draw(self):
        # Test that run calls handle_events and draw
        
        # Create a mock for the window methods
        original_handle_events = self.window.handle_events
        original_draw = self.window.draw
        
        handle_events_called = False
        draw_called = False
        
        def mock_handle_events():
            nonlocal handle_events_called
            handle_events_called = True
            # Return False to exit the run loop immediately
            return False
            
        def mock_draw():
            nonlocal draw_called
            draw_called = True
        
        # Replace methods with mocks
        self.window.handle_events = mock_handle_events
        self.window.draw = mock_draw
        
        try:
            # Run the window (should exit immediately due to mock_handle_events)
            with patch('pygame.quit'):
                self.window.run()
                
            # Check that both methods were called
            self.assertTrue(handle_events_called)
            self.assertTrue(draw_called)
            
        finally:
            # Restore original methods
            self.window.handle_events = original_handle_events
            self.window.draw = original_draw
