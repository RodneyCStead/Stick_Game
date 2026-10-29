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

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    game_canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_engine = GameEngine(game_canvas)

    print("Game initialized for web deployment")

    def get_canvas_transform():
        display_width, display_height = display.get_size()
        scale = min(display_width / SCREEN_WIDTH, display_height / SCREEN_HEIGHT)
        scaled_width = int(SCREEN_WIDTH * scale)
        scaled_height = int(SCREEN_HEIGHT * scale)
        offset_x = (display_width - scaled_width) // 2
        offset_y = (display_height - scaled_height) // 2
        return scale, offset_x, offset_y

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                scale, offset_x, offset_y = get_canvas_transform()
                canvas_x = (event.pos[0] - offset_x) / scale
                canvas_y = (event.pos[1] - offset_y) / scale
                if 0 <= canvas_x <= SCREEN_WIDTH and 0 <= canvas_y <= SCREEN_HEIGHT:
                    event.pos = (int(canvas_x), int(canvas_y))
                    game_engine.handle_event(event)
            else:
                game_engine.handle_event(event)

        game_engine.update()
        game_engine.render()

        scale, offset_x, offset_y = get_canvas_transform()
        scaled_canvas = pygame.transform.smoothscale(
            game_canvas,
            (max(1, int(SCREEN_WIDTH * scale)), max(1, int(SCREEN_HEIGHT * scale))),
        )
        display.fill(BLACK)
        display.blit(scaled_canvas, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(FPS)
        
        # Allow other async operations (important for web)
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
