# filepath: /home/sparky/code/PyUI/pyui/widgets/nine_patch.py
import json

from pathlib import Path
from pygame import Surface
from dataclasses import dataclass

from pyui.widget import Widget
from pyui.helpers import Size, Position
from pyui.assets import get_nine_patch, ASSETS_FOLDER


@dataclass
class NinePatchData:
    """
    Stores the sizes of the nine patch corners and the associated image
    """
    top: int
    bottom: int
    left: int
    right: int
    image: Surface = None
    
    @classmethod
    def from_json(cls, json_name: str):            
        json_path = ASSETS_FOLDER / "nine_patch" / json_name
        if not json_path.exists():
            raise FileNotFoundError(f"Nine patch JSON '{json_name}' not found in assets.")
            
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Create the instance with corner measurements
        instance = cls(top=data.get('top', 0),
                       bottom=data.get('bottom', 0),
                       left=data.get('left', 0),
                       right=data.get('right', 0))
        
        # Extract the base name without extension
        base_name = Path(json_name).stem
        image_name = f"{base_name}.png"
        instance.image = get_nine_patch(image_name)
        return instance


class NinePatch(Widget):
    """
    A widget that displays a nine-patch image which can be expanded to 
    fit different sizes while preserving its corner appearance
    """
    def __init__(self, nine_patch_data: NinePatchData, **kwargs):
        super().__init__(**kwargs)
        # Set the minimum size based on corners
        self.min_width = self.nine_patch_data.left + self.nine_patch_data.right
        self.min_height = self.nine_patch_data.top + self.nine_patch_data.bottom
        # This widget is self-expanding by default
        self.expanding = True
    
    @property
    def min_size(self) -> Size:
        return Size(self.min_width, self.min_height) + self.margin.size
    
    def render(self, destination: Surface, position: Position, size: Size):
        """
        Render the nine patch image to the given surface at the specified position.
        Stretches the center parts to fit the given size while preserving corners.
        """
        render_pos = self.get_position(size)
        render_pos += position
        # Add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        
        # Calculate render size (subtract margins)
        render_width = size.width - self.margin.left - self.margin.right
        render_height = size.height - self.margin.top - self.margin.bottom
        
        # Ensure minimum size requirements
        render_width = max(render_width, self.min_width)
        render_height = max(render_height, self.min_height)
        
        # Create a new surface for the nine-patch rendering
        patch_surface = Surface((render_width, render_height))
        
        # Get patch sizes
        n = self.nine_patch_data
        img_width = self.image.get_width()
        img_height = self.image.get_height()
        
        # Draw the corners (they remain the same size)
        # Top-left corner
        patch_surface.blit(self.image.subsurface((0, 0, n.left, n.top)), (0, 0))
        patch_surface.blit(self.image.subsurface((img_width - n.right, 0, n.right, n.top)),
                           (render_width - n.right, 0))
        patch_surface.blit(self.image.subsurface((0, img_height - n.bottom, n.left, n.bottom)),
                           (0, render_height - n.bottom))
        patch_surface.blit(self.image.subsurface((img_width - n.right, img_height - n.bottom, n.right, n.bottom)),
            (render_width - n.right, render_height - n.bottom))
        
        # Top edge
        top_edge = self.image.subsurface((n.left, 0, img_width - n.left - n.right, n.top))
        scaled_top_edge = Surface.scale(top_edge, (render_width - n.left - n.right, n.top))
        patch_surface.blit(scaled_top_edge, (n.left, 0))
        
        # Bottom edge
        bottom_edge = self.image.subsurface((n.left, img_height - n.bottom, 
                                            img_width - n.left - n.right, n.bottom))
        scaled_bottom_edge = Surface.scale(bottom_edge, (render_width - n.left - n.right, n.bottom))
        patch_surface.blit(scaled_bottom_edge, (n.left, render_height - n.bottom))
        
        # Left edge
        left_edge = self.image.subsurface((0, n.top, n.left, img_height - n.top - n.bottom))
        scaled_left_edge = Surface.scale(left_edge, (n.left, render_height - n.top - n.bottom))
        patch_surface.blit(scaled_left_edge, (0, n.top))
        
        # Right edge
        right_edge = self.image.subsurface((img_width - n.right, n.top, n.right, img_height - n.top - n.bottom))
        scaled_right_edge = Surface.scale(right_edge, (n.right, render_height - n.top - n.bottom))
        patch_surface.blit(scaled_right_edge, (render_width - n.right, n.top))
        
        # Center section
        center = self.image.subsurface((n.left, n.top, img_width - n.left - n.right,
                                        img_height - n.top - n.bottom))
        scaled_center = Surface.scale(center, 
                                    (render_width - n.left - n.right, 
                                     render_height - n.top - n.bottom))
        patch_surface.blit(scaled_center, (n.left, n.top))
        destination.blit(patch_surface, (render_pos.x, render_pos.y))
