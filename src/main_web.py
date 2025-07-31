"""
Web-optimized main entry point for GitHub Pages deployment
Optimized for browser compatibility and performance
"""

import pygame
import asyncio
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import *
from game.engine import GameEngine
from ui.renderer import Renderer
from utils.input_handler import InputHandler
from utils.viewport_manager import ViewportManager

async def main():
    """Main game loop optimized for web deployment"""
    pygame.init()
    pygame.display.set_caption("Stick It To Em - Card Battle Game")
    
    # Start with a reasonable default size for web
    # Viewport will handle scaling automatically
    initial_width = min(1200, 1024)  # Limit initial size for web
    initial_height = min(800, 600)
    
    screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    
    # Initialize viewport manager for responsive scaling
    viewport = ViewportManager(screen)
    
    # Initialize game systems
    renderer = Renderer(screen, viewport)
    input_handler = InputHandler()
    game_engine = GameEngine(renderer, input_handler, clock)
    
    print(f"Game initialized for web deployment")
    print(f"Initial size: {initial_width}x{initial_height}")
    print(f"Viewport: {viewport.base_width}x{viewport.base_height}, Scale: {viewport.scale_x:.2f}x{viewport.scale_y:.2f}, Uniform: {viewport.uniform_scale:.2f}")
    
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize for responsive design
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                game_engine.update_screen(screen)
                print(f"Resized to: {event.w}x{event.h}")
                print(f"New viewport scale: {viewport.scale_x:.2f}x{viewport.scale_y:.2f}, Uniform: {viewport.uniform_scale:.2f}")
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
