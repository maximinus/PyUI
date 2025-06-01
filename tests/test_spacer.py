from unittest.mock import MagicMock, patch

from pyui.test_helper import PyuiTest
from pyui.helpers import Size, Expand
from pyui.widget import Widget
from pyui.widgets import Spacer


class TestSpacer(PyuiTest):    
    def test_initialization_horizontal(self):
        """Test Spacer initialization with horizontal expansion."""
        spacer = Spacer(expand=Expand.HORIZONTAL)
        self.assertEqual(spacer.expand, Expand.HORIZONTAL)
        
    def test_initialization_vertical(self):
        """Test Spacer initialization with vertical expansion."""
        spacer = Spacer(expand=Expand.VERTICAL)
        self.assertEqual(spacer.expand, Expand.VERTICAL)
        
    def test_initialization_both(self):
        """Test Spacer initialization with both directions expansion."""
        spacer = Spacer(expand=Expand.BOTH)
        self.assertEqual(spacer.expand, Expand.BOTH)
        
    def test_initialization_none(self):
        """Test Spacer initialization with no expansion."""
        spacer = Spacer(expand=Expand.NONE)
        self.assertEqual(spacer.expand, Expand.NONE)
        
    def test_inheritance(self):
        """Test that Spacer inherits from Widget."""
        spacer = Spacer(expand=Expand.NONE)
        self.assertIsInstance(spacer, Widget)
    
    def test_min_size_with_expand_both(self):
        """Test min_size with Expand.BOTH setting."""
        spacer = Spacer(expand=Expand.BOTH)
        self.assertEqual(spacer.min_size, Size(0, 0))
        
    def test_min_size_with_expand_none(self):
        """Test min_size with Expand.NONE setting."""
        spacer = Spacer(expand=Expand.NONE)
        self.assertEqual(spacer.min_size, Size(0, 0))
