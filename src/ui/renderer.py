"""
Main Renderer - Handles all game rendering for Stick It To Em
"""

import pygame
from utils.constants import *
from utils.image_loader import image_loader

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
    
    def render_battle(self, battle_state):
        """Render the entire battle scene"""
        # Render platform
        self._render_platform()
        
        # Render characters
        self._render_character(battle_state.player, PLAYER_COLOR)
        self._render_character(battle_state.enemy, ENEMY_COLOR)
        
        # Render health bars
        self._render_health_bar(battle_state.player, 50, 50)
        self._render_health_bar(battle_state.enemy, SCREEN_WIDTH - 250, 50)
        
        # Render bottom panel
        self._render_bottom_panel()
        
        # Render player's hand
        self._render_hand(battle_state.player.hand)
        
        # Render turn indicator
        self._render_turn_indicator(battle_state.get_current_turn())
        
        # Render enemy intent
        self._render_enemy_intent(battle_state.enemy)
        
        # Render battle end screen if needed
        if battle_state.battle_over:
            self._render_battle_end(battle_state.winner)
    
    def _render_platform(self):
        """Render the battle platform"""
        # Try to load platform image, fallback to colored rectangle
        platform_image = image_loader.load_platform("battlefield", (SCREEN_WIDTH - 200, PLATFORM_HEIGHT))
        platform_rect = pygame.Rect(100, PLATFORM_Y, SCREEN_WIDTH - 200, PLATFORM_HEIGHT)
        self.screen.blit(platform_image, platform_rect)
    
    def _render_character(self, character, color):
        """Render a stick figure character"""
        # Try to load character sprite, fallback to colored rectangle
        character_image = image_loader.load_character(character.name, (60, 120))
        char_rect = character_image.get_rect(center=(character.x, character.y))
        self.screen.blit(character_image, char_rect)
        
        # Render character name
        name_text = self.font.render(character.name, True, TEXT_COLOR)
        name_rect = name_text.get_rect(center=(character.x, character.y - 80))
        self.screen.blit(name_text, name_rect)
    
    def _render_health_bar(self, character, x, y):
        """Render a health bar for a character"""
        bar_width = 200
        bar_height = 20
        
        # Background
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, DARK_GRAY, bg_rect)
        
        # Health bar
        health_percent = character.get_health_percentage()
        health_width = int(bar_width * health_percent)
        health_rect = pygame.Rect(x, y, health_width, bar_height)
        pygame.draw.rect(self.screen, HEALTH_COLOR, health_rect)
        
        # Border
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
        
        # Health text
        health_text = f"{character.health}/{character.max_health}"
        text_surface = self.font.render(health_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.screen.blit(text_surface, text_rect)
    
    def _render_bottom_panel(self):
        """Render the bottom UI panel"""
        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect)
        pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, 2)
    
    def _render_hand(self, hand):
        """Render the player's hand of cards"""
        if not hand:
            return
        
        # Calculate card positions
        total_width = len(hand) * CARD_WIDTH + (len(hand) - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, card in enumerate(hand):
            card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            self._render_card(card, card_x, HAND_Y)
    
    def _render_card(self, card, x, y):
        """Render a single card with stick figure art"""
        # Try to load card artwork, fallback to simple design
        card_image = image_loader.load_card(card.name, (CARD_WIDTH, CARD_HEIGHT))
        self.screen.blit(card_image, (x, y))
        
        # Overlay card information on top of the artwork
        # Card cost (top-left corner)
        cost_bg = pygame.Surface((25, 25))
        cost_bg.fill(MANA_COLOR)
        cost_bg.set_alpha(200)
        self.screen.blit(cost_bg, (x + 5, y + 5))
        
        cost_text = self.font.render(str(card.cost), True, WHITE)
        cost_rect = cost_text.get_rect(center=(x + 17, y + 17))
        self.screen.blit(cost_text, cost_rect)
        
        # Card name at bottom
        name_bg = pygame.Surface((CARD_WIDTH - 10, 25))
        name_bg.fill(BLACK)
        name_bg.set_alpha(180)
        self.screen.blit(name_bg, (x + 5, y + CARD_HEIGHT - 30))
        
        name_text = self.small_font.render(card.name, True, WHITE)
        name_rect = name_text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT - 17))
        self.screen.blit(name_text, name_rect)
    
    def _render_wrapped_text(self, text, x, y, width, color):
        """Render text with word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.small_font.size(test_line)[0] <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines[:4]):  # Max 4 lines
            line_surface = self.small_font.render(line, True, color)
            self.screen.blit(line_surface, (x, y + i * 20))
    
    def _render_turn_indicator(self, current_turn):
        """Render whose turn it is"""
        turn_text = f"{current_turn.title()}'s Turn"
        text_surface = self.title_font.render(turn_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(text_surface, text_rect)
    
    def _render_enemy_intent(self, enemy):
        """Render what the enemy plans to do"""
        intent_text = enemy.get_intent()
        text_surface = self.font.render(intent_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(enemy.x, enemy.y + 80))
        self.screen.blit(text_surface, text_rect)
    
    def _render_battle_end(self, winner):
        """Render battle end screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        result_text = "Victory!" if winner == "player" else "Defeat!"
        text_surface = self.title_font.render(result_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
