import unittest

from pyui.base import Margin
from pyui.widgets import Image


class MockImage():
    def __init__(self):
        pass

    def get_width(self):
        return 256

    def get_height(self):
        return 256


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = MockImage()

    def test_size(self):
        img = Image(self.image)
        self.assertEqual(img.size.width, 256)
        self.assertEqual(img.size.height, 256)

    def test_min_size(self):
        img = Image(self.image)
        min_size = img.min_size
        self.assertEqual(min_size.width, 256)
        self.assertEqual(min_size.height, 256)

    def test_size_with_margin(self):
        img = Image(self.image, margin=Margin(22, 22, 22, 22))
        self.assertEqual(img.size.width, 256)
        self.assertEqual(img.size.height, 256)

    def test_min_size_wuth_margin(self):
        img = Image(self.image, margin=Margin(22, 22, 22, 22))
        min_size = img.min_size
        self.assertEqual(min_size.width, 300)
        self.assertEqual(min_size.height, 300)
