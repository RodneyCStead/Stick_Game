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
from ui.renderer import Renderer
from utils.input_handler import InputHandler

async def main():
    """Main game loop optimized for web deployment"""
    pygame.init()
    pygame.display.set_caption("Stick It To Em - Card Battle Game")
    
    # For web deployment, start with base size and allow scaling
    screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Initialize game systems (without viewport for now to avoid import issues)
    renderer = Renderer(screen)
    input_handler = InputHandler()
    game_engine = GameEngine(renderer, input_handler, clock)
    
    print(f"Game initialized for web deployment")
    print(f"Screen size: {DEFAULT_SCREEN_WIDTH}x{DEFAULT_SCREEN_HEIGHT}")
    
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
        clock.tick(FPS)
        
        # Critical for web deployment - yield control to browser
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
