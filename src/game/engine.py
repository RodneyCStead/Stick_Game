"""Game Engine - Manages game loop and state"""

import pygame
from utils.constants import *
from utils.input_handler import InputHandler
from game.battle import BattleState
from entities.enemy import Enemy
from ui.renderer import Renderer


class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.input_handler = InputHandler()
        self.renderer = Renderer(screen)

        # Game state tracking
        self.current_state = "battle"
        self.battle_index = 0
        self.battles = self._create_battles()
        self.battle_state = self.battles[self.battle_index]

        # Debug / error capture
        self.last_error = None
        print(f"[GameEngine] Initialized with {len(self.battles)} battle(s)")

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        self.input_handler.update(event)
        if self.current_state == "battle":
            self.battle_state.handle_input(self.input_handler)

    def update(self):
        try:
            if self.current_state == "battle":
                self.battle_state.update()
                if self.battle_state.battle_over and self.battle_state.winner == "player":
                    if self.battle_index + 1 < len(self.battles):
                        self.battle_index += 1
                        self.battle_state = self.battles[self.battle_index]
                        print(f"[GameEngine] Advancing to battle {self.battle_index + 1}")
                    else:
                        self.current_state = "game_complete"
                        print("[GameEngine] All battles complete")
        except Exception as e:
            import traceback
            self.last_error = ''.join(traceback.format_exception_only(type(e), e)).strip()
            print('[GameEngine][ERROR][update]', self.last_error)
        self.input_handler.reset_frame()

    def update_screen(self, new_screen):
        self.screen = new_screen
        self.renderer.update_screen(new_screen)
        if hasattr(self.battle_state, 'update_character_positions'):
            self.battle_state.update_character_positions()

    def render(self):
        self.screen.fill(BLACK)
        try:
            if self.current_state == "battle":
                self.renderer.render_battle(self.battle_state)
            elif self.current_state == "game_complete":
                self._render_game_complete()
        except Exception as e:
            import traceback
            self.last_error = ''.join(traceback.format_exception_only(type(e), e)).strip()
            print('[GameEngine][ERROR][render]', self.last_error)

        if self.last_error:
            err_font = pygame.font.Font(None, 28)
            surf = err_font.render(self.last_error[:60], True, (255, 50, 50))
            self.screen.blit(surf, (10, 10))

        self._render_debug_info()

    def _render_debug_info(self):
        # Placeholder for future debug info
        pass

    def _create_battles(self):
        player = None
        battles = []
        b1 = BattleState(player=player, enemies=[Enemy("Green Slime")])
        player = b1.player
        battles.append(b1)
        b2 = BattleState(player=player, enemies=[Enemy("Green Slime"), Enemy("Blue Slime")])
        battles.append(b2)
        return battles

    def _render_game_complete(self):
        msg = self.font.render("All Battles Won!", True, TEXT_COLOR)
        rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(msg, rect)
