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
    
    def load_image(self, image_path, size=None, fallback_color=(255, 255, 255), make_transparent=False, transparent_color=(255, 255, 255)):
        """
        Load an image with caching and fallback
        
        Args:
            image_path: Path relative to assets/sprites/
            size: Tuple (width, height) to scale the image
            fallback_color: Color to use if image not found
            make_transparent: Whether to make a specific color transparent
            transparent_color: Color to make transparent (default: white)
        
        Returns:
            pygame.Surface: The loaded (and optionally scaled) image
        """
        # Create cache key
        cache_key = f"{image_path}_{size}_{make_transparent}"
        
        # Return cached image if available
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        full_path = os.path.join(self.base_path, image_path)
        
        try:
            # Try to load the image
            image = pygame.image.load(full_path)
            print(f"Successfully loaded: {full_path}")  # Debug output
            
            # Convert to a format that supports transparency
            if make_transparent:
                image = image.convert()
                image.set_colorkey(transparent_color)  # Make white transparent
            else:
                image = image.convert_alpha()
            
            # Scale if size provided
            if size:
                image = pygame.transform.scale(image, size)
            
            # Cache and return
            self.image_cache[cache_key] = image
            return image
            
        except (pygame.error, FileNotFoundError) as e:
            print(f"Failed to load: {full_path} - Error: {e}")  # Debug output
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
        """Load a card image with white background made transparent"""
        # Custom mapping for specific card names to file names
        card_file_mapping = {
            "slash": "slash_Attack.png",
            "kick": "kick_Attack.png",
            "healing": "healing_Utility.jpg",
            "shield": "shield_Enhancement.jpg"
        }
        
        # Cards that should NOT have white transparency (like shields with white elements)
        no_transparency_cards = ["shield"]
        
        # Get the correct filename
        card_key = card_name.lower()
        if card_key in card_file_mapping:
            filename = card_file_mapping[card_key]
        else:
            # Fallback to old naming convention
            filename = card_name.lower().replace(" ", "_").replace("'", "") + ".png"
        
        image_path = f"cards/{filename}"
        
        # Check if this card should have transparency or not
        if card_key in no_transparency_cards:
            # Don't make white transparent for shield cards
            return self.load_image(image_path, size, make_transparent=False)
        else:
            # TEMPORARILY DISABLE transparency for ALL cards to debug white-out issue
            return self.load_image(image_path, size, make_transparent=False)
            # Original line: return self.load_image(image_path, size, make_transparent=True, transparent_color=(255, 255, 255))
    
    def load_ui_element(self, element_name, size=None):
        """Load a UI element - tries multiple file extensions, NO transparency"""
        # Try different file extensions
        extensions = ['.png', '.jpg', '.jpeg']
        
        for ext in extensions:
            try:
                image_path = f"ui/{element_name.lower()}{ext}"
                full_path = os.path.join(self.base_path, image_path)
                if os.path.exists(full_path):
                    # Load WITHOUT transparency for UI elements
                    return self.load_image(image_path, size, make_transparent=False)
            except:
                continue
        
        # If no file found, create fallback
        if size:
            fallback = pygame.Surface(size)
        else:
            fallback = pygame.Surface((100, 100))
        fallback.fill((64, 64, 64))  # Dark gray fallback
        return fallback
    
    def load_platform(self, platform_name="battlefield", size=(1000, 200)):
        """Load platform/background image"""
        image_path = f"platform/{platform_name.lower()}.png"
        return self.load_image(image_path, size)

# Global image loader instance
image_loader = ImageLoader()
