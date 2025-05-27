import pygame
from pathlib import Path
from typing import Dict

ASSETS_FOLDER = Path(__file__).parent / "assets"


class FileCache:
    def __init__(self):
        self.images: Dict[str, pygame.Surface] = {}
        self.nine_patch: Dict[str, pygame.Surface] = {}

    def clear(self):
        self.images = {}
        self.nine_patch = {}


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
    image = pygame.image.load(image_path)
    file_cache.images[image_name] = image
    return image


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
    nine_patch = pygame.image.load(patch_path)
    file_cache.nine_patch[patch_name] = nine_patch
    return nine_patch


def get_nine_patch_data(json_name: str):
    """Get NinePatchData from a JSON file in the assets folder."""
    from pyui.widgets.nine_patch import NinePatchData
    return NinePatchData.from_json(json_name)
