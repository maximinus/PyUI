import pygame
from pathlib import Path
from typing import Dict

from pyui.helpers import Size


ASSETS_FOLDER = Path(__file__).parent / "assets"


class Font:
    """
    A class that represents a font for rendering text.
    """
    def __init__(self, font_name: str, size: int = 16):
        """
        Initialize a Font object.
        Args:
            font_name: Name of the font or path to a font file
            size: Font size in points
        """
        from pyui.assets import ASSETS_FOLDER
        font_path = ASSETS_FOLDER / "fonts" / font_name
        self.font = pygame.font.Font(str(font_path), size)
        self.size = size

    def render(self, text, color=(0, 0, 0)):
        """Render text using the font."""
        return self.font.render(text, True, color)
    
    def size_of(self, text) -> Size:
        """Get the size of rendered text."""
        pygame_size = self.font.size(text)
        return Size(pygame_size[0], pygame_size[1])


class FileCache:
    def __init__(self):
        self.images: Dict[str, pygame.Surface] = {}
        self.nine_patch: Dict[str, pygame.Surface] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.icons: Dict[str, pygame.Surface] = {}

    def clear(self):
        self.images = {}
        self.nine_patch = {}
        self.icons = {}
        self.fonts = {}


file_cache = FileCache()


def get_image(image_name: str) -> pygame.Surface:
    """Get an image from the assets folder, using cache if available."""
    # Check if the image is already in the cache
    if image_name in file_cache.images:
        return file_cache.images[image_name]
    
    # Load the image if not in cache
    image_path = ASSETS_FOLDER / "images" / image_name
    if not image_path.exists():
        raise FileNotFoundError(f"Image '{image_name}' not found in assets.")
    
    # Load the image and store in cache
    image = pygame.image.load(image_path).convert_alpha()
    file_cache.images[image_name] = image
    return image


def get_icon(image_name: str) -> pygame.Surface:
    """Get an image from the assets folder, using cache if available."""
    # Check if the image is already in the cache
    if image_name in file_cache.icons:
        return file_cache.icons[image_name]
    
    # Load the image if not in cache
    icon_path = ASSETS_FOLDER / "icons" / image_name
    if not icon_path.exists():
        raise FileNotFoundError(f"Icon '{image_name}' not found in assets.")
    
    # Load the image and store in cache
    icon = pygame.image.load(icon_path).convert_alpha()
    file_cache.icons[image_name] = icon
    return icon


def get_nine_patch(patch_name: str) -> pygame.Surface:
    """Get a nine patch from the assets folder, using cache if available."""
    # Check if the nine patch is already in the cache
    if patch_name in file_cache.nine_patch:
        return file_cache.nine_patch[patch_name]
    
    # Load the nine patch if not in cache
    patch_path = ASSETS_FOLDER / "nine_patch" / patch_name
    if not patch_path.exists():
        raise FileNotFoundError(f"Nine patch '{patch_name}' not found in assets.")
    
    # Load the nine patch and store in cache
    nine_patch = pygame.image.load(patch_path).convert_alpha()
    file_cache.nine_patch[patch_name] = nine_patch
    return nine_patch


def get_nine_patch_data(json_name: str):
    """Get NinePatchData from a JSON file in the assets folder."""
    from pyui.widgets.nine_patch import NinePatchData
    return NinePatchData.from_json(json_name)


def get_font(font_name: str, size: int = 16) -> Font:
    font_key = f"{font_name}_{size}"
    if font_key in file_cache.fonts:
        return file_cache.fonts[font_key]
    font_path = ASSETS_FOLDER / "fonts" / font_name
    font = Font(font_path, size)
    file_cache.fonts[font_key] = font
    return font
