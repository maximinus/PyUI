from pyui.helpers import Position

class TextStore:
    def __init__(self):
        self.lines = []
        self.cursor = Position(0, 0)
    
    def insert_char(self, char: str):
        """Insert text at the current cursor position."""
        self.lines[self.cursor.y].insert(self.cursor.x, char)
        self.cursor.x += 1
    
    def remove_char(self):
        """Remove the character at the current cursor position."""
        if self.cursor.x > 0:
            self.lines[self.cursor.y].pop(self.cursor.x - 1)
            self.cursor.x -= 1
        elif self.cursor.y > 0:
            prev_line = self.lines[self.cursor.y - 1]
            self.cursor.x = len(prev_line)
            self.lines[self.cursor.y - 1].extend(self.lines.pop(self.cursor.y))
            self.cursor.y -= 1
    
    def overwrite_char(self, char: str):
        """Overwrite the character at the current cursor position."""
        if self.cursor.x < len(self.lines[self.cursor.y]):
            self.lines[self.cursor.y][self.cursor.x] = char
        else:
            self.insert_char(char)
