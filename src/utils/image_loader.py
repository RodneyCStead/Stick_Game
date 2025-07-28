"""
Image loading utilities for Stick It To Em
Handles loading, caching, and error handling for game assets
"""

import pygame
import os

class ImageLoader:
    def __init__(self):
        self.image_cache = {}
        self.base_path = "assets/sprites"
    
    def load_image(self, image_path, size=None, fallback_color=(255, 255, 255)):
        """
        Load an image with caching and fallback
        
        Args:
            image_path: Path relative to assets/sprites/
            size: Tuple (width, height) to scale the image
            fallback_color: Color to use if image not found
        
        Returns:
            pygame.Surface: The loaded (and optionally scaled) image
        """
        # Create cache key
        cache_key = f"{image_path}_{size}"
        
        # Return cached image if available
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        full_path = os.path.join(self.base_path, image_path)
        
        try:
            # Try to load the image
            image = pygame.image.load(full_path)
            
            # Scale if size provided
            if size:
                image = pygame.transform.scale(image, size)
            
            # Cache and return
            self.image_cache[cache_key] = image
            return image
            
        except (pygame.error, FileNotFoundError):
            # Create fallback rectangle if image not found
            if size:
                fallback = pygame.Surface(size)
            else:
                fallback = pygame.Surface((60, 120))  # Default character size
            
            fallback.fill(fallback_color)
            
            # Cache the fallback
            self.image_cache[cache_key] = fallback
            return fallback
    
    def load_character(self, character_name, size=(60, 120)):
        """Load a character sprite"""
        image_path = f"characters/{character_name.lower()}.png"
        return self.load_image(image_path, size)
    
    def load_card(self, card_name, size=(120, 160)):
        """Load a card image"""
        # Convert card name to filename (remove spaces, lowercase)
        filename = card_name.lower().replace(" ", "_").replace("'", "")
        image_path = f"cards/{filename}.png"
        return self.load_image(image_path, size)
    
    def load_ui_element(self, element_name, size=None):
        """Load a UI element"""
        image_path = f"ui/{element_name.lower()}.png"
        return self.load_image(image_path, size)
    
    def load_platform(self, platform_name="battlefield", size=(1000, 200)):
        """Load platform/background image"""
        image_path = f"platform/{platform_name.lower()}.png"
        return self.load_image(image_path, size)

# Global image loader instance
image_loader = ImageLoader()
