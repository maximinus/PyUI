from unittest.mock import MagicMock, patch

from pyui.test_helper import PyuiTest
from pyui.window import Window
from pyui.helpers import Mouse


class TestMouseInteractions(PyuiTest):
    def setUp(self):
        self.window = Window.default()
        
    def tearDown(self):
        self.window.running = False
    
    def test_draw_called_after_events(self):
        """Test that draw is called after handle_events in the main loop."""
        # Create mocks to track call order
        call_order = []
        
        # Store original methods
        original_handle_events = self.window.handle_events
        original_draw = self.window.draw
        
        # Replace with tracking versions
        def mock_handle_events():
            call_order.append('handle_events')
            # Exit after first loop
            return False
            
        def mock_draw():
            call_order.append('draw')
        
        self.window.handle_events = mock_handle_events
        self.window.draw = mock_draw
        
        try:
            # Run the window (should exit after one loop)
            with patch('pygame.quit'):
                self.window.run()
                
            # Expected order: initial draw, then handle_events, then draw again
            self.assertEqual(call_order, ['draw', 'handle_events', 'draw'])
            
        finally:
            # Restore original methods
            self.window.handle_events = original_handle_events
            self.window.draw = original_draw
    
    def test_fps_control(self):
        """Test that FPS control is used in the main loop."""
        with patch('pygame.time.Clock') as mock_clock:
            mock_clock_instance = MagicMock()
            mock_clock.return_value = mock_clock_instance
            
            # Setup window to exit immediately
            with patch.object(self.window, 'handle_events', return_value=False), \
                 patch('pygame.quit'):
                self.window.run()
            
            # Verify clock was used with correct FPS
            mock_clock_instance.tick.assert_called_with(30)  # Using FRAMES_PER_SECOND constant
