"""
Web-optimized main entry point for GitHub Pages deployment
Optimized for browser compatibility and performance
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
    
    # Start with base game size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Initialize game engine (it creates its own renderer and input handler)
    game_engine = GameEngine(screen)
    
    print(f"Game initialized for web deployment")
    print(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                game_engine.screen = screen
                game_engine.renderer.screen = screen
                print(f"Resized to: {event.w}x{event.h}")
            else:
                game_engine.handle_event(event)
        
        # Update and render
        game_engine.update()
        game_engine.render()
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Allow other async operations (important for web)
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
