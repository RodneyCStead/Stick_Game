"""
Game Constants
Screen dimensions, colors, and other game settings
"""

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
DEFAULT_SCREEN_WIDTH = 1200  # Base design width for viewport scaling
DEFAULT_SCREEN_HEIGHT = 800  # Base design height for viewport scaling
BASE_WIDTH = DEFAULT_SCREEN_WIDTH  # Alias for compatibility
BASE_HEIGHT = DEFAULT_SCREEN_HEIGHT  # Alias for compatibility
FPS = 30

# Game layout
PLATFORM_WIDTH = 1216  
PLATFORM_HEIGHT = 240
PLATFORM_Y = SCREEN_HEIGHT - PLATFORM_HEIGHT - 200  
BOTTOM_PANEL_HEIGHT = 250  

# Background layout
BACKGROUND_WIDTH = SCREEN_WIDTH  
BACKGROUND_HEIGHT = PLATFORM_Y  
BACKGROUND_X = 0
BACKGROUND_Y = 0  

# Deck position
DECK_X = 20
DECK_Y = SCREEN_HEIGHT - 160 - DECK_X
DECK_WIDTH = 120
DECK_HEIGHT = 160

# END TURN button position (moved to where discard was)
END_TURN_X = 160
END_TURN_Y = SCREEN_HEIGHT - 160 - 20  # 20 pixels from bottom
END_TURN_WIDTH = 120
END_TURN_HEIGHT = 160

# Character positions
PLAYER_X = 400
ENEMY_X = SCREEN_WIDTH - 400
CHARACTER_Y = PLATFORM_Y - 160  
ENEMY_Y = PLATFORM_Y - 80       

# Card display
CARD_WIDTH = 120
CARD_HEIGHT = 160
CARD_SPACING = 10
CARDS_PER_ROW = 4
HAND_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 80  

# Card info display area - individual element positioning for each element
CARD_INFO_WIDTH = 275

#Card info font sizes
CARD_NAME_FSIZE = 60      
CARD_AP_FSIZE = 40        
CARD_DESC_FSIZE = 30      
CARD_FLAVOR_FSIZE = 30       

# Card name position
CARD_NAME_X = SCREEN_WIDTH - 280  
CARD_NAME_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 10  

# AP cost position
CARD_AP_X = SCREEN_WIDTH - 280
CARD_AP_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 70

# Description position
CARD_DESC_X = SCREEN_WIDTH - 280 
CARD_DESC_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 100  

# Flavor text position
CARD_FLAVOR_X = SCREEN_WIDTH - 280  
CARD_FLAVOR_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 140    

# Deck counter position
DECK_COUNTER_X = 30  
DECK_COUNTER_Y = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT + 20

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0,255,0)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Platform colors
PLATFORM_COLOR = (139, 69, 19)  # Brown
PLATFORM_BORDER = (101, 50, 13)  # Dark brown

# UI colors
PANEL_COLOR = BLACK
PANEL_BORDER = BLACK
CARD_COLOR = WHITE
CARD_BORDER = BLACK
CARD_SELECTED = YELLOW

# Text colors
TEXT_COLOR = WHITE
HEALTH_COLOR = RED    
AP_COLOR = GREEN 

# Card info text colors
CARD_NAME_COLOR = BLACK         # Black text for light brown background
CARD_AP_COLOR = GREEN          
CARD_DESC_COLOR = BLACK         # Black text for light brown background
CARD_FLAVOR_COLOR = DARK_GRAY   # Dark gray for flavor text          
