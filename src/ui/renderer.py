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
        # Render background (first layer)
        self._render_background()
        
        # Render platform (middle layer)
        self._render_platform()
        
        # Render characters
        self._render_player(battle_state.player)
        self._render_slime(battle_state.enemy)
        
        # Render health bars
        self._render_health_bar(battle_state.player, 50, 50)
        self._render_health_bar(battle_state.enemy, SCREEN_WIDTH - 250, 50)
        
        # Render bottom panel
        self._render_bottom_panel()
        
        # Render deck image
        self._render_deck_image()
        
        # Render end turn button
        self._render_end_turn_button()
        
        # Render player's hand
        self._render_hand(battle_state.player.hand, battle_state)
        
        # Render player's action points
        self._render_action_points(battle_state.player)
        
        # Render deck counter
        self._render_deck_counter(battle_state.player)
        
        # Render card info display
        self._render_card_info_display(battle_state)
        
        # Render turn indicator
        self._render_turn_indicator(battle_state.get_current_turn())
        
        # Render enemy intent
        self._render_enemy_intent(battle_state.enemy)
        
        # Render battle end screen if needed
        if battle_state.battle_over:
            self._render_battle_end(battle_state.winner)
    
    # Helper methods for rendering various components
    def _render_background(self):
        """Render the background from top of screen to where platform starts"""
        background_image = image_loader.load_background("background_Box.png", (BACKGROUND_WIDTH, BACKGROUND_HEIGHT), make_transparent=False)
        background_rect = pygame.Rect(BACKGROUND_X, BACKGROUND_Y, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        self.screen.blit(background_image, background_rect)
    
    def _render_platform(self):
        """Render the battle platform"""
        platform_image = image_loader.load_image("platform/platform_Box.png", (PLATFORM_WIDTH, PLATFORM_HEIGHT), make_transparent=True, transparent_color=(255, 255, 255))
        
        # Centers the platform on screen
        platform_x = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
        platform_rect = pygame.Rect(platform_x, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.screen.blit(platform_image, platform_rect)
    
    def _render_player(self, player):
        """Render the player character with specific sizing and positioning"""
        # Player-specific character size
        player_size = (100, 240)  
        player_image = image_loader.load_character(player.name, player_size, state="idle")
        player_rect = player_image.get_rect(center=(player.x, player.y))
        self.screen.blit(player_image, player_rect)
        
        # Render player name
        name_text = self.font.render(player.name, True, TEXT_COLOR)
        name_rect = name_text.get_rect(center=(player.x, player.y - 140))  # Adjusted for player size
        self.screen.blit(name_text, name_rect)
    
    def _render_slime(self, slime):
        """Render the slime enemy with specific sizing and positioning"""
        # Slime-specific character size (different from player)
        slime_size = (80, 120)  # Smaller than player
        slime_image = image_loader.load_character("slime", slime_size, state="idle")
        slime_rect = slime_image.get_rect(center=(slime.x, slime.y))
        self.screen.blit(slime_image, slime_rect)
        
        # Render slime name
        name_text = self.font.render("Slime", True, TEXT_COLOR)
        name_rect = name_text.get_rect(center=(slime.x, slime.y - 80))  # Adjusted for slime size
        self.screen.blit(name_text, name_rect)
    
    def _render_health_bar(self, character, x, y):
        """Render a health bar and armor for a character"""
        bar_width = 200
        bar_height = 20
        
        # Health bar background
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
        
        # Armor display (if any)
        if hasattr(character, 'armor') and character.armor > 0:
            armor_text = f"Armor: {character.armor}"
            armor_surface = self.small_font.render(armor_text, True, (150, 150, 255))
            self.screen.blit(armor_surface, (x, y + bar_height + 5))
        
        # Buffs display
        if hasattr(character, 'buffs') and character.buffs:
            buff_y = y + bar_height + 25
            for buff_name, buff_data in character.buffs.items():
                buff_text = f"{buff_name.title()}: +{buff_data['value']} ({buff_data['duration']} turns)"
                buff_surface = self.small_font.render(buff_text, True, (255, 255, 150))
                self.screen.blit(buff_surface, (x, buff_y))
                buff_y += 15
    
    def _render_deck_image (self):
        """Render the deck representation image in bottom left corner"""
        deck_image = image_loader.load_image("cards/Stickittoem_backing.png", (DECK_WIDTH, DECK_HEIGHT), make_transparent=False)
        deck_rect = pygame.Rect(DECK_X, DECK_Y, DECK_WIDTH, DECK_HEIGHT)
        self.screen.blit(deck_image, deck_rect)
        
        # Draws a black border around deck image
        pygame.draw.rect(self.screen, BLACK, deck_rect, 2)
        
    def _render_end_turn_button(self):
        """Render the END TURN button in bottom right corner"""
        # Try to load END TURN button image, fallback to text button
        try:
            end_turn_image = image_loader.load_image("ui/end_Turn_Button.png", (END_TURN_WIDTH, END_TURN_HEIGHT), make_transparent=False)
            end_turn_rect = pygame.Rect(END_TURN_X, END_TURN_Y, END_TURN_WIDTH, END_TURN_HEIGHT)
            self.screen.blit(end_turn_image, end_turn_rect)
        except:
            # Fallback to text-based button
            end_turn_rect = pygame.Rect(END_TURN_X, END_TURN_Y, END_TURN_WIDTH, END_TURN_HEIGHT)
            pygame.draw.rect(self.screen, (100, 100, 100), end_turn_rect)  # Gray background
            pygame.draw.rect(self.screen, WHITE, end_turn_rect, 2)  # White border
            
            # Add "END TURN" text
            button_text = self.font.render("END", True, WHITE)
            turn_text = self.font.render("TURN", True, WHITE)
            
            # Center the text in the button
            text_x = END_TURN_X + (END_TURN_WIDTH - button_text.get_width()) // 2
            text_y1 = END_TURN_Y + (END_TURN_HEIGHT // 2) - 20
            text_y2 = END_TURN_Y + (END_TURN_HEIGHT // 2) + 5
            
            self.screen.blit(button_text, (text_x, text_y1))
            self.screen.blit(turn_text, (text_x, text_y2))

        # Draw black border around button
        button_rect = pygame.Rect(END_TURN_X, END_TURN_Y, END_TURN_WIDTH, END_TURN_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)

    def _render_bottom_panel(self):
        """Render the bottom UI panel with background image"""
        panel_rect = pygame.Rect(0, SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL_HEIGHT)
        
        # Load PNG background image, fallback to colored rectangle
        try:
            panel_background = image_loader.load_image("ui/bottom_Box.png", (SCREEN_WIDTH, BOTTOM_PANEL_HEIGHT))
            self.screen.blit(panel_background, (0, SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT))
        except:
            # Fallback to original colored panel
            pygame.draw.rect(self.screen, PANEL_COLOR, panel_rect)
            pygame.draw.rect(self.screen, PANEL_BORDER, panel_rect, 2)
    
    def _render_hand(self, hand, battle_state):
        """Render the player's hand of cards"""
        if not hand:
            return
        
        # Calculate card positions
        total_width = len(hand) * CARD_WIDTH + (len(hand) - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, card in enumerate(hand):
            card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            is_selected = (battle_state.selected_card_index == i)
            self._render_card(card, card_x, HAND_Y, is_selected)
    
    def _render_card(self, card, x, y, is_selected=False):
        """Render a single card with stick figure art"""
        # Try to load card artwork first
        card_image = image_loader.load_card(card.name, (CARD_WIDTH, CARD_HEIGHT))
        
        # Blit the card image
        self.screen.blit(card_image, (x, y))
        
        # Draw a border around the card
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        if is_selected:
            # Highlight selected card with thicker, colored border
            pygame.draw.rect(self.screen, (255, 255, 0), card_rect, 4)  # Yellow border
        else:
            # Normal black border
            pygame.draw.rect(self.screen, BLACK, card_rect, 2)
        
    
    def _render_action_points(self, player):
        """Render the player's action points"""
        ap_text = f"AP: {player.action_points}/{player.max_action_points}"
        ap_font = pygame.font.Font(None,36)
        text_surface = self.font.render(ap_text, True, AP_COLOR)
        
        # Position in bottom-left of screen
        ap_x = 200
        ap_y = SCREEN_HEIGHT - 230
        self.screen.blit(text_surface, (ap_x, ap_y))
    
    def _render_deck_counter(self, player):
        """Render the deck card counter"""
        deck_count = player.deck.cards_remaining()
        
        deck_text = f"Deck: {deck_count} / 10"
        
        # Use constants for positioning
        deck_surface = self.font.render(deck_text, True, WHITE)
        
        self.screen.blit(deck_surface, (DECK_COUNTER_X, DECK_COUNTER_Y))
    
    def _render_card_info_display(self, battle_state):
        """Render the card information display with individual positioning for each element"""
        # Check if we have a selected card to display
        if battle_state.selected_card_info:
            card_info = battle_state.selected_card_info
            
            # Font sizes for card info
            card_name_font = pygame.font.Font(None, CARD_NAME_FSIZE)
            card_ap_font = pygame.font.Font(None, CARD_AP_FSIZE)
            card_desc_font = pygame.font.Font(None, CARD_DESC_FSIZE)
            card_flavor_font = pygame.font.Font(None, CARD_FLAVOR_FSIZE)
            
            # Card name (at specified position)
            # Replace self.font with the specific font for each element
            name_text = card_name_font.render(card_info['name'], True, CARD_NAME_COLOR)
            self.screen.blit(name_text, (CARD_NAME_X, CARD_NAME_Y))

            # AP cost (at specified position)
            cost_text = f"AP Cost: {card_info['cost']}"
            cost_surface = card_ap_font.render(cost_text, True, CARD_AP_COLOR)
            self.screen.blit(cost_surface, (CARD_AP_X, CARD_AP_Y))
            
            # Description (wrapped text at specified position)
            self._render_wrapped_text(card_info['description'], CARD_DESC_X, CARD_DESC_Y, CARD_INFO_WIDTH, CARD_DESC_COLOR, card_desc_font)
            
            # Flavor text (wrapped text at specified position)
            if card_info.get('flavor_text'):
                self._render_wrapped_text(card_info['flavor_text'], CARD_FLAVOR_X, CARD_FLAVOR_Y, CARD_INFO_WIDTH, CARD_FLAVOR_COLOR, card_flavor_font)

    def _render_wrapped_text(self, text, x, y, width, color, font=None):
        """Render text with word wrapping"""
        if font is None:
            font = self.small_font  # Default font
            
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines[:4]):  
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (x, y + i * 22))  # Increased line spacing for larger fonts
    
    def _calculate_wrapped_lines(self, text, width, font=None):
        """Calculate how many lines wrapped text will take"""
        if font is None:
            font = self.small_font  # Default font
            
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
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
