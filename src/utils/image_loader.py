"""
Image loading utilities for Stick It To Em
Handles loading, caching, and error handling for game assets
"""

import pygame
import os

class ImageLoader:
    def __init__(self):
        self.image_cache = {}
        # Get the project root directory (go up from src/utils/ to project root)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.base_path = os.path.join(project_root, "assets", "sprites")
    
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
            
            # Convert to a format that supports transparency
            if make_transparent:
                image = image.convert()
                image.set_colorkey(transparent_color)  
            else:
                image = image.convert_alpha()
            
            # Scale if size provided
            if size:
                image = pygame.transform.scale(image, size)
            
            # Cache and return
            self.image_cache[cache_key] = image
            return image
            
        except (pygame.error, FileNotFoundError) as e:
            # Create fallback rectangle if image not found
            if size:
                fallback = pygame.Surface(size)
            else:
                fallback = pygame.Surface((60, 120))  # Default character size
            
            fallback.fill(fallback_color)
            
            # Cache the fallback
            self.image_cache[cache_key] = fallback
            return fallback
    
    def load_character(self, character_name, size=(80, 120), state="idle"):
        """Load a character sprite with animation state support"""
    
        # Normalize provided character_name to match actual filename patterns.
        # Assets currently use mixed case like green_Slime_Idle.png, blue_Slime_Idle.png
        name_normalized = character_name.replace(" ", "_")
        if name_normalized in ("Green_Slime", "green_slime"):
            char_name = "green_Slime"
        elif name_normalized in ("Blue_Slime", "blue_slime"):
            char_name = "blue_Slime"
        else:
            # Fallback: lowercase (works if assets are fully lowercase)
            char_name = name_normalized.lower()
        anim_state = state.lower()
        
        # Define custom transparent colors for specific characters
        character_transparent_colors = {
            "player": (0, 0, 255),
            "green_slime": (0, 0, 255),
            "green_Slime": (0, 0, 255),
            "blue_slime": (0, 0, 255),
            "blue_Slime": (0, 0, 255)
        }
        
        # Get the transparent color for this character (default to white)
        transparent_color = character_transparent_colors.get(char_name, (255, 255, 255))
        
        # Try character with animation state first (e.g., "player_Idle.png")
        image_path = f"characters/{char_name}_{anim_state.title()}.png"
        
        # Check if the specific animation state exists
        full_path = os.path.join(self.base_path, image_path)
        
        if os.path.exists(full_path):
            # Load with character-specific background transparency
            return self.load_image(image_path, size, make_transparent=True, transparent_color=transparent_color)
        
        # Fallback to basic character name (e.g., "player.png")
        fallback_path = f"characters/{char_name}.png"
        print(f"DEBUG LOADER: Fallback to: {fallback_path}")
        return self.load_image(fallback_path, size, make_transparent=True, transparent_color=transparent_color)
    
    def load_card(self, card_name, size=(120, 160)):
        
        # Custom mapping for specific card names to file names
        card_file_mapping = {
            "slash": "slash_Attack.png",
            "kick": "kick_Attack.png",
            "healing": "healing_Utility.png",
            "shield": "shield_Enhancement.png",
            "glorp": "glorp_Attack.png",
            "blorp": "blorp_Attack.png",
            "slime shield": "slimeshield_Enhancement.png"
        }
                
        # Get the correct filename
        card_key = card_name.lower()
        if card_key in card_file_mapping:
            filename = card_file_mapping[card_key]
        else:
            # Fallback to old naming convention
            filename = card_name.lower().replace(" ", "_").replace("'", "") + ".png"
        
        image_path = f"cards/{filename}"
        
        # No transparency for cards since they have no backgrounds to remove
        return self.load_image(image_path, size, make_transparent=False)
    
    def load_ui_element(self, element_name, size=None):
        """Load assets/sprites/ui or assets/ui, preserving the requested filename."""
        extensions = ['.png', '.jpg', '.jpeg']

        project_root = os.path.dirname(os.path.dirname(self.base_path))
        search_roots = [
            (self.base_path, "ui"),
            (os.path.join(project_root, "assets"), "ui"),
        ]

        for root, subfolder in search_roots:
            for ext in extensions:
                image_path = os.path.join(subfolder, element_name + ext)
                full_path = os.path.join(root, image_path)
                if os.path.exists(full_path):
                    image = pygame.image.load(full_path)
                    if size:
                        image = pygame.transform.scale(image, size)
                    return image.convert_alpha()

        if size:
            fallback = pygame.Surface(size)
        else:
            fallback = pygame.Surface((100, 100))
        fallback.fill((64, 64, 64))
        return fallback
    
    def load_platform(self, platform_name="battlefield", size=(1000, 200)):
        """Load platform/background image"""
        image_path = f"platform/{platform_name.lower()}.png"
        return self.load_image(image_path, size)

    def load_background(self, background_name, size=None, make_transparent=False, transparent_color=(255, 255, 255)):
        """Load background image from assets/backgrounds/ folder"""
        # Create cache key
        cache_key = f"bg_{background_name}_{size}_{make_transparent}"
        
        # Return cached image if available
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # Use absolute path for backgrounds
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        full_path = os.path.join(project_root, "assets", "backgrounds", background_name)
        
        try:
            # Try to load the image
            image = pygame.image.load(full_path)
            
            # Convert to a format that supports transparency
            if make_transparent:
                image = image.convert()
                image.set_colorkey(transparent_color)
            else:
                image = image.convert_alpha()
            
            # Scale if size provided
            if size:
                image = pygame.transform.scale(image, size)
            
            # Cache and return
            self.image_cache[cache_key] = image
            return image
            
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load background: {full_path} - {e}")
            # Create fallback rectangle if image not found
            if size:
                fallback = pygame.Surface(size)
            else:
                fallback = pygame.Surface((1200, 400))  # Default background size
            
            fallback.fill((135, 206, 235))  # Sky blue fallback
            
            # Cache the fallback
            self.image_cache[cache_key] = fallback
            return fallback

# Global image loader instance
image_loader = ImageLoader()
