import unittest

from pyui.helpers import Position
from pyui.text.text_store import TextStore


class TestTextStore(unittest.TestCase):
    def setUp(self):
        self.text_store = TextStore()
        # Initialize with one empty line for basic tests
        self.text_store.lines = [[]]
        self.text_store.cursor = Position(0, 0)

    def test_init(self):
        """Test the initialization of TextStore."""
        text_store = TextStore()
        self.assertEqual(text_store.lines, [])
        self.assertEqual(text_store.cursor, Position(0, 0))

    def test_insert_char(self):
        """Test inserting a character at cursor position."""
        self.text_store.insert_char('a')
        self.assertEqual(self.text_store.lines[0], ['a'])
        self.assertEqual(self.text_store.cursor.x, 1)
        self.assertEqual(self.text_store.cursor.y, 0)

    def test_insert_multiple_chars(self):
        """Test inserting multiple characters in sequence."""
        self.text_store.insert_char('a')
        self.text_store.insert_char('b')
        self.text_store.insert_char('c')
        self.assertEqual(self.text_store.lines[0], ['a', 'b', 'c'])
        self.assertEqual(self.text_store.cursor.x, 3)

    def test_remove_char_from_middle(self):
        """Test removing a character from the middle of a line."""
        self.text_store.lines[0] = ['a', 'b', 'c']
        self.text_store.cursor = Position(2, 0)
        
        self.text_store.remove_char()
        self.assertEqual(self.text_store.lines[0], ['a', 'c'])
        self.assertEqual(self.text_store.cursor.x, 1)
        self.assertEqual(self.text_store.cursor.y, 0)

    def test_remove_char_from_start(self):
        """Test that removing a character at the start of a line does nothing."""
        self.text_store.lines[0] = ['a', 'b', 'c']
        self.text_store.cursor = Position(0, 0)
        
        self.text_store.remove_char()
        self.assertEqual(self.text_store.lines[0], ['a', 'b', 'c'])
        self.assertEqual(self.text_store.cursor.x, 0)
        self.assertEqual(self.text_store.cursor.y, 0)

    def test_remove_char_across_lines(self):
        """Test removing a character at the start of a line joins with previous line."""
        self.text_store.lines = [['a', 'b'], ['c', 'd']]
        self.text_store.cursor = Position(0, 1)
        
        self.text_store.remove_char()
        self.assertEqual(self.text_store.lines, [['a', 'b', 'c', 'd']])
        self.assertEqual(self.text_store.cursor.x, 2)
        self.assertEqual(self.text_store.cursor.y, 0)

    def test_remove_char_from_empty_line(self):
        """Test removing a character from an empty line removes the line."""
        self.text_store.lines = [['a', 'b'], []]
        self.text_store.cursor = Position(0, 1)
        
        self.text_store.remove_char()
        self.assertEqual(self.text_store.lines, [['a', 'b']])
        self.assertEqual(self.text_store.cursor.x, 2)
        self.assertEqual(self.text_store.cursor.y, 0)

    def test_overwrite_char_in_middle(self):
        """Test overwriting a character in the middle of a line."""
        self.text_store.lines[0] = ['a', 'b', 'c']
        self.text_store.cursor = Position(1, 0)
        
        self.text_store.overwrite_char('x')
        self.assertEqual(self.text_store.lines[0], ['a', 'x', 'c'])
        self.assertEqual(self.text_store.cursor.x, 1)  # Cursor should not move after overwrite

    def test_overwrite_char_at_end(self):
        """Test overwriting a character at the end of a line inserts instead."""
        self.text_store.lines[0] = ['a', 'b', 'c']
        self.text_store.cursor = Position(3, 0)
        
        self.text_store.overwrite_char('x')
        self.assertEqual(self.text_store.lines[0], ['a', 'b', 'c', 'x'])
        self.assertEqual(self.text_store.cursor.x, 4)  # Cursor should move after insert

    def test_overwrite_char_empty_line(self):
        """Test overwriting a character on an empty line inserts instead."""
        self.text_store.overwrite_char('x')
        self.assertEqual(self.text_store.lines[0], ['x'])
        self.assertEqual(self.text_store.cursor.x, 1)


if __name__ == '__main__':
    unittest.main()
