"""
Web-optimized main entry point for GitHub Pages deployment
Compatible with pygbag for browser deployment
"""

import pygame
import asyncio
import sys
import os

# Add src directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from utils.constants import *
from game.engine import GameEngine

async def main():
    """Main game loop optimized for web deployment"""
    pygame.init()
    pygame.display.set_caption("Stick It To Em - Card Battle Game")
    
    # For web deployment, start with base size and allow scaling
    screen = pygame.display.set_mode((1200, 800))  # Use hardcoded values
    clock = pygame.time.Clock()
    
    # Initialize game engine (it creates its own renderer and input handler)
    game_engine = GameEngine(screen)
    
    print(f"Game initialized for web deployment")
    print(f"Screen size: 1200x800")
    
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_engine.handle_event(event)
        
        # Update and render
        game_engine.update()
        game_engine.render()
        
        pygame.display.flip()
        clock.tick(30)  # Use hardcoded FPS
        
        # Critical for web deployment - yield control to browser
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
