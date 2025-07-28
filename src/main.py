"""
Stick It To Em - Main Entry Point
A turn-based stick figure card battle game
"""

import pygame
import asyncio
from game.engine import GameEngine
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

async def main():
    """Main game loop"""
    pygame.init()
    
    # Sets up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stick It To Em - Card Battle")
    clock = pygame.time.Clock()
    
    # Initializes the game engine
    game_engine = GameEngine(screen)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_engine.handle_event(event)
        
        # Update game state
        game_engine.update()
        
        # Render everything
        game_engine.render()
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
        
        # Required for pygbag web deployment
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
