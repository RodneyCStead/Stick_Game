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

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Stick It To Em - Card Battle")
    game_canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_engine = GameEngine(game_canvas)

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
        display.fill((0, 0, 0))
        display.blit(scaled_canvas, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
