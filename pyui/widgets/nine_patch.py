# filepath: /home/sparky/code/PyUI/pyui/widgets/nine_patch.py
import json

from pathlib import Path
from pygame import Surface
from pygame import transform
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
    fit different sizes while preserving its corner appearance.
    
    The nine-patch can be sized either based on its corner measurements (minimum)
    or with an explicit minimum size provided through the size parameter.
    """
    def __init__(self, nine_patch_data: NinePatchData, size: Size = None, **kwargs):
        super().__init__(**kwargs)
        self.nine_patch_data = nine_patch_data
        self.render_image = nine_patch_data.image
        self.img_size = Size(self.render_image.get_width(), self.render_image.get_height())
        if size:
            self.size = size
        else:
            self.size = Size(self.nine_patch_data.left + self.nine_patch_data.right,
                             self.nine_patch_data.top + self.nine_patch_data.bottom)
        # This widget is self-expanding by default
        self.expanding = True
    
    @property
    def min_size(self) -> Size:
        return self.size + self.margin.size

    def render(self, destination: Surface, position: Position, size: Size):
        """
        Render the nine patch image to the given surface at the specified position.
        Stretches the center parts to fit the given size while preserving corners.
        """
        if self.image.matches(size):
            destination.blit(self.image, position)
            return

        new_image = self.get_new_image(size)
        render_pos = self.get_position(size)
        # Add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        
        # Calculate render size (subtract margins)
        render_width = self.size.width
        if self.expand.horizontal:
            render_width = size.width - self.margin.width
        render_height = self.size.height
        if self.expand.vertical:
            render_height = size.height - self.margin.height
        
        # Create a new surface for the nine-patch rendering
        patch_surface = Surface((render_width, render_height))
        n = self.nine_patch_data
        
        # Draw the corners (they remain the same size)
        # Top-left corner
        patch_surface.blit(self.render_image.subsurface((0, 0, n.left, n.top)), (0, 0))
        patch_surface.blit(self.render_image.subsurface((self.img_size.width - n.right, 0, n.right, n.top)),
                           (render_width - n.right, 0))
        patch_surface.blit(self.render_image.subsurface((0, self.img_size.height - n.bottom, n.left, n.bottom)),
                           (0, render_height - n.bottom))
        patch_surface.blit(self.render_image.subsurface(
            (self.img_size.width - n.right, self.img_size.height - n.bottom, n.right, n.bottom)),
            (render_width - n.right, render_height - n.bottom))
        
        # Top edge
        top_edge = self.render_image.subsurface((n.left, 0, self.img_size.width - n.left - n.right, n.top))
        scaled_top_edge = transform.scale(top_edge, (render_width - n.left - n.right, n.top))
        patch_surface.blit(scaled_top_edge, (n.left, 0))
        
        # Bottom edge
        bottom_edge = self.render_image.subsurface((n.left, self.img_size.height - n.bottom, 
                                            self.img_size.width - n.left - n.right, n.bottom))
        scaled_bottom_edge = transform.scale(bottom_edge, (render_width - n.left - n.right, n.bottom))
        patch_surface.blit(scaled_bottom_edge, (n.left, render_height - n.bottom))
        
        # Left edge
        left_edge = self.render_image.subsurface((0, n.top, n.left, self.img_size.height - n.top - n.bottom))
        scaled_left_edge = transform.scale(left_edge, (n.left, render_height - n.top - n.bottom))
        patch_surface.blit(scaled_left_edge, (0, n.top))
        
        # Right edge
        right_edge = self.render_image.subsurface((self.img_size.width - n.right, n.top, n.right, self.img_size.height - n.top - n.bottom))
        scaled_right_edge = transform.scale(right_edge,
                                            (n.right, render_height - n.top - n.bottom))
        patch_surface.blit(scaled_right_edge, (render_width - n.right, n.top))
        # Center section
        center = self.render_image.subsurface((n.left, n.top, self.img_size.width - n.left - n.right,
                                        self.img_size.height - n.top - n.bottom))
        scaled_center = transform.scale(center, 
                                    (render_width - n.left - n.right, 
                                     render_height - n.top - n.bottom))
        patch_surface.blit(scaled_center, (n.left, n.top))
        new_image.blit(patch_surface, (render_pos.x, render_pos.y))
        self.image.update(new_image)
        destination.blit(new_image, position.as_tuple)
