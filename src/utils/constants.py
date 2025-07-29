"""
Game Constants
Screen dimensions, colors, and other game settings
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Game layout
PLATFORM_HEIGHT = 200
PLATFORM_Y = SCREEN_HEIGHT - PLATFORM_HEIGHT - 200  # Increased space for larger bottom panel
BOTTOM_PANEL_HEIGHT = 200  # Increased from 150 to 200

# Character positions
PLAYER_X = 200
ENEMY_X = SCREEN_WIDTH - 200
CHARACTER_Y = PLATFORM_Y - 100

# Card display
CARD_WIDTH = 120
CARD_HEIGHT = 160
CARD_SPACING = 10
CARDS_PER_ROW = 5
HAND_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 20  # Moved higher up in the bottom panel

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# Platform colors
PLATFORM_COLOR = (139, 69, 19)  # Brown
PLATFORM_BORDER = (101, 50, 13)  # Dark brown

# UI colors
PANEL_COLOR = (50, 50, 50)
PANEL_BORDER = (100, 100, 100)
CARD_COLOR = (200, 200, 200)
CARD_BORDER = (100, 100, 100)
CARD_SELECTED = (255, 255, 0)  # Yellow

# Character colors (placeholder)
PLAYER_COLOR = (0, 100, 255)  # Blue
ENEMY_COLOR = (255, 50, 50)   # Red

# Text colors
TEXT_COLOR = WHITE
HEALTH_COLOR = (255, 0, 0)    # Red
MANA_COLOR = (0, 0, 255)      # Blue
