"""Game Engine - Manages overall game state and loop.

Includes a between-battle transition that pauses and displays
"Round N" before spawning the next battle wave.
"""

import time
import pygame
from utils.constants import *
from utils.input_handler import InputHandler
from game.battle import BattleState
from entities.enemy import Enemy
from ui.renderer import Renderer


class GameEngine:
    def __init__(self, screen):
        # Core
        self.screen = screen
        self.input_handler = InputHandler()
        self.renderer = Renderer(screen)

        # Battles
        self.current_state = "battle"  # battle | transition | game_complete
        self.battle_index = 0
        self.battles = self._create_battles()
        self.battle_state = self.battles[self.battle_index]

        # Transition data
        self.transition_start_time: float | None = None
        self.transition_delay = 2.0  # seconds
        self.transition_target_index: int | None = None
        self.transition_message: str | None = None

        # Error / debug
        self.last_error = None

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        print(f"[GameEngine] Initialized with {len(self.battles)} battle(s)")

    # -------------------------------------------------
    # Event Handling
    # -------------------------------------------------
    def handle_event(self, event):
        self.input_handler.update(event)
        if self.current_state == "battle":
            self.battle_state.handle_input(self.input_handler)
        # For transition we still gather input (skip handled in update)

    # -------------------------------------------------
    # Update Loop
    # -------------------------------------------------
    def update(self):
        try:
            if self.current_state == "battle":
                self.battle_state.update()
                if self.battle_state.battle_over and self.battle_state.winner == "player":
                    if self.battle_index + 1 < len(self.battles):
                        self._start_transition(self.battle_index + 1)
                    else:
                        self.current_state = "game_complete"
                        print("[GameEngine] All battles complete")
            elif self.current_state == "transition":
                self._update_transition()
        except Exception as e:
            import traceback
            self.last_error = ''.join(traceback.format_exception_only(type(e), e)).strip()
            print('[GameEngine][ERROR][update]', self.last_error)
        self.input_handler.reset_frame()

    # -------------------------------------------------
    # Render Loop
    # -------------------------------------------------
    def render(self):
        self.screen.fill(BLACK)
        try:
            if self.current_state == "battle":
                self.renderer.render_battle(self.battle_state)
            elif self.current_state == "transition":
                # Render last battle scene (victory overlay handled by renderer) then overlay round text
                self.renderer.render_battle(self.battle_state)
                self._render_transition_overlay()
            elif self.current_state == "game_complete":
                self._render_game_complete()
        except Exception as e:
            import traceback
            self.last_error = ''.join(traceback.format_exception_only(type(e), e)).strip()
            print('[GameEngine][ERROR][render]', self.last_error)

        # Error overlay (simple)
        if self.last_error:
            err_font = pygame.font.Font(None, 28)
            surf = err_font.render(self.last_error[:60], True, (255, 50, 50))
            self.screen.blit(surf, (10, 10))

        self._render_debug_info()

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def update_screen(self, new_screen):
        self.screen = new_screen
        self.renderer.update_screen(new_screen)
        if hasattr(self.battle_state, 'update_character_positions'):
            self.battle_state.update_character_positions()

    def _render_debug_info(self):  # placeholder
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

    # -------------------------------------------------
    # Transition Logic
    # -------------------------------------------------
    def _start_transition(self, target_index: int):
        self.current_state = "transition"
        self.transition_start_time = time.time()
        self.transition_target_index = target_index
        self.transition_message = f"Round {target_index + 1}"
        print(f"[GameEngine] Transition starting -> {self.transition_message}")

    def _update_transition(self):
        elapsed = time.time() - (self.transition_start_time or 0)
        user_skip = (self.input_handler.is_mouse_clicked() or
                     self.input_handler.is_mouse_double_clicked() or
                     bool(self.input_handler.keys_pressed))
        if elapsed >= self.transition_delay or user_skip:
            self._advance_to_battle()

    def _advance_to_battle(self):
        if self.transition_target_index is None:
            return
        self.battle_index = self.transition_target_index
        self.battle_state = self.battles[self.battle_index]
        self.current_state = "battle"
        # Clear transition info
        self.transition_start_time = None
        self.transition_target_index = None
        self.transition_message = None
        print(f"[GameEngine] Advancing to battle {self.battle_index + 1}")

    def _render_transition_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        if not self.transition_message:
            return
        title_font = pygame.font.Font(None, 96)
        msg_surface = title_font.render(self.transition_message, True, TEXT_COLOR)
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(msg_surface, msg_rect)

        sub_font = pygame.font.Font(None, 36)
        remaining = max(0, int(self.transition_delay - (time.time() - (self.transition_start_time or 0)) + 1))
        sub_text = f"Starting in {remaining}s - click to skip"
        sub_surface = sub_font.render(sub_text, True, TEXT_COLOR)
        sub_rect = sub_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        self.screen.blit(sub_surface, sub_rect)
