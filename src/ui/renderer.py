import pygame
from utils.constants import *
from utils.image_loader import image_loader
from utils.animation_manager import animation_manager

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        # Removed self.viewport = viewport
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
    
    def update_screen(self, new_screen):
        """Update screen reference when screen changes"""
        self.screen = new_screen
        # Removed all viewport code
    
    def render_battle(self, battle_state):
        """Render the entire battle scene"""
        # Update animation system
        animation_manager.update()

        # Layered scene
        self._render_background()
        self._render_platform()

        # Characters
        self._render_player(battle_state.player)
        if hasattr(battle_state, 'enemies'):
            for enemy in battle_state.get_active_enemies():
                self._render_slime(enemy, battle_state)
        else:  # fallback single enemy attr
            self._render_slime(battle_state.enemy, battle_state)

        # Player top-left health bar (keeping for quick glance)
        self._render_health_bar(battle_state.player, 50, 50)

        # UI foundation
        self._render_bottom_panel()
        self._render_deck_image()
        self._render_end_turn_button()
        self._render_hand(battle_state.player.hand, battle_state)

        # New centered player status bars above hand
        self._render_player_status_bars(battle_state.player)

        # Other stats & info
        self._render_action_points(battle_state.player)
        self._render_deck_counter(battle_state.player)
        self._render_card_info_display(battle_state)
        self._render_turn_indicator(battle_state.get_current_turn())

        # Targeting indicator
        if getattr(battle_state, 'selected_enemy', None):
            self._render_target_arrow(battle_state.selected_enemy)

        # Battle end overlay
        if battle_state.battle_over:
            self._render_battle_end(battle_state.winner)
    
    # Helper methods for rendering various components
    def _render_background(self):
        """Render the background from top of screen to where platform starts"""
        background_image = image_loader.load_background("background_Box.png", (BACKGROUND_WIDTH, BACKGROUND_HEIGHT), make_transparent=False)
        background_rect = pygame.Rect(BACKGROUND_X, BACKGROUND_Y, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        self.screen.blit(background_image, background_rect)
    
    def _render_platform(self):
        """Render the battle platform with safe fallback"""
        try:
            platform_image = image_loader.load_image(
                "platform/platform_Box.png",
                (PLATFORM_WIDTH, PLATFORM_HEIGHT),
                make_transparent=True,
                transparent_color=(255, 255, 255)
            )
        except Exception as e:
            # Fallback plain surface so a missing asset doesn't crash web build
            print(f"PLATFORM LOAD FAIL fallback used: {e}")
            platform_image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            platform_image.fill((90,90,90))
            pygame.draw.rect(platform_image, (0,0,0), platform_image.get_rect(), 2)
        platform_x = (SCREEN_WIDTH - PLATFORM_WIDTH) // 2
        platform_rect = pygame.Rect(platform_x, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.screen.blit(platform_image, platform_rect)
    
    def _render_player(self, player):
        """Render the player character with specific sizing and positioning"""
        # Player-specific character size
        player_size = (200, 280)  
        
        # Get current animation state
        animation_state = animation_manager.get_character_state('player')
        
        player_image = image_loader.load_character(player.name, player_size, state=animation_state)
        player_rect = player_image.get_rect(center=(player.x, player.y))
        self.screen.blit(player_image, player_rect)
        
        # Render player name
        name_text = self.font.render(player.name, True, TEXT_COLOR)
        name_rect = name_text.get_rect(center=(player.x, player.y - 140))  # Adjusted for player size
        self.screen.blit(name_text, name_rect)
    
    def _render_slime(self, slime, battle_state):
        """Render the slime enemy with specific sizing and positioning.
        Only the targeted enemy shows hit animation (Slashed/Kicked). Others stay Idle during attack resolution."""
        slime_size = (140, 160)
        base_state = animation_manager.get_character_state('enemy')
        # Determine if this enemy should display the base_state or idle
        display_state = base_state
        if base_state in ("Slashed", "Kicked"):
            # Only show on targeted enemy
            if animation_manager.current_enemy_target is not slime:
                display_state = "Idle"
        slime_name_for_file = slime.name.replace(" ", "_")
        slime_image = image_loader.load_character(slime_name_for_file, slime_size, state=display_state)
        slime_rect = slime_image.get_rect(center=(slime.x, slime.y))
        self.screen.blit(slime_image, slime_rect)
        name_text = self.font.render(slime.name, True, TEXT_COLOR)
        name_rect = name_text.get_rect(center=(slime.x, slime.y - 80))
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

    # Renders the deck card counter
    def _render_deck_counter(self, player):
        deck_count = player.deck.cards_remaining()
        deck_text = f"Deck: {deck_count} / 10"
        
        # Use constants for positioning
        deck_surface = self.font.render(deck_text, True, WHITE)
        
        self.screen.blit(deck_surface, (DECK_COUNTER_X, DECK_COUNTER_Y))

    # Renders the card (or enemy) information panel bottom-right.
    def _render_card_info_display(self, battle_state):
        
        # Priority: card info over enemy info
        if battle_state.selected_card_info:
            info = battle_state.selected_card_info
            name_font = pygame.font.Font(None, CARD_NAME_FSIZE)
            ap_font = pygame.font.Font(None, CARD_AP_FSIZE)
            desc_font = pygame.font.Font(None, CARD_DESC_FSIZE)
            flavor_font = pygame.font.Font(None, CARD_FLAVOR_FSIZE)
            name_text = name_font.render(info['name'], True, CARD_NAME_COLOR)
            self.screen.blit(name_text, (CARD_NAME_X, CARD_NAME_Y))
            cost_text = f"AP Cost: {info['cost']}"
            cost_surface = ap_font.render(cost_text, True, CARD_AP_COLOR)
            self.screen.blit(cost_surface, (CARD_AP_X, CARD_AP_Y))
            self._render_wrapped_text(info['description'], CARD_DESC_X, CARD_DESC_Y, CARD_INFO_WIDTH, CARD_DESC_COLOR, desc_font)
           
            if info.get('flavor_text'):
                self._render_wrapped_text(info['flavor_text'], CARD_FLAVOR_X, CARD_FLAVOR_Y, CARD_INFO_WIDTH, CARD_FLAVOR_COLOR, flavor_font)
        
        elif getattr(battle_state, 'selected_enemy', None):
            enemy = battle_state.selected_enemy
            name_font = pygame.font.Font(None, CARD_NAME_FSIZE)
            bar_font = pygame.font.Font(None, 28)
            flavor_font = pygame.font.Font(None, CARD_FLAVOR_FSIZE)
            name_surface = name_font.render(enemy.name, True, CARD_NAME_COLOR)
            self.screen.blit(name_surface, (CARD_NAME_X, CARD_NAME_Y))
            bar_x = CARD_DESC_X
            bar_y = CARD_AP_Y
            bar_w = CARD_INFO_WIDTH - 20
            bar_h = 24
            
            pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_w, bar_h))
            hp_pct = enemy.get_health_percentage()
            pygame.draw.rect(self.screen, HEALTH_COLOR, (bar_x, bar_y, int(bar_w * hp_pct), bar_h))
            pygame.draw.rect(self.screen, BLACK, (bar_x, bar_y, bar_w, bar_h), 2)
            hp_text = bar_font.render(f"HP {enemy.health}/{enemy.max_health}", True, TEXT_COLOR)
            self.screen.blit(hp_text, (bar_x + 6, bar_y + 2))
            
            armor_y = bar_y + bar_h + 8
            armor_color_bg = (40, 60, 90)
            armor_fill_color = (120, 180, 255)
            pygame.draw.rect(self.screen, armor_color_bg, (bar_x, armor_y, bar_w, bar_h))
            max_armor = max(enemy.armor, 1)
            
            if enemy.armor > 0:
                fill_w = int(bar_w * (enemy.armor / max_armor))
                pygame.draw.rect(self.screen, armor_fill_color, (bar_x, armor_y, fill_w, bar_h))
                
            pygame.draw.rect(self.screen, BLACK, (bar_x, armor_y, bar_w, bar_h), 2)
            armor_text = bar_font.render(f"Armor {enemy.armor}", True, TEXT_COLOR)
            self.screen.blit(armor_text, (bar_x + 6, armor_y + 2))
            if hasattr(enemy, 'flavor_text') and enemy.flavor_text:
                self._render_wrapped_text(enemy.flavor_text, CARD_FLAVOR_X, CARD_FLAVOR_Y, CARD_INFO_WIDTH, CARD_FLAVOR_COLOR, flavor_font)

    # Renders a red triangle pointing down to indicate clearly to the player which enemy is selected
    def _render_target_arrow(self, enemy):
        
        arrow_height = 40
        arrow_width = 60
        tip_x = enemy.x
        tip_y = enemy.y - 100  # point just above enemy sprite
        base_y = tip_y - arrow_height
        points = [
            (tip_x, tip_y),  
            (tip_x - arrow_width//2, base_y),
            (tip_x + arrow_width//2, base_y)
        ]
        pygame.draw.polygon(self.screen, (255,0,0), points)
        pygame.draw.polygon(self.screen, (0,0,0), points, 4)
        
    # Render player status bars
    def _render_player_status_bars(self, player):
        bar_w = 250
        bar_h = 24
        spacing = 30
        total_width = bar_w * 2 + spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        # Position so the bottom of the bars sits just above the top border of the card area
        panel_top = SCREEN_HEIGHT - BOTTOM_PANEL_HEIGHT
        gap = 4
        y = panel_top - bar_h - gap

        # Health bar
        hb_x = start_x
        pygame.draw.rect(self.screen, DARK_GRAY, (hb_x, y, bar_w, bar_h))
        hp_pct = player.get_health_percentage()
        pygame.draw.rect(self.screen, HEALTH_COLOR, (hb_x, y, int(bar_w * hp_pct), bar_h))
        pygame.draw.rect(self.screen, BLACK, (hb_x, y, bar_w, bar_h), 2)
        hp_text = self.font.render(f"HP {player.health}/{player.max_health}", True, TEXT_COLOR)
        self.screen.blit(hp_text, (hb_x + 6, y + 2))

        # Armor bar
        ab_x = hb_x + bar_w + spacing
        armor_bg = (40, 60, 90)
        armor_fill = (120, 180, 255)
        pygame.draw.rect(self.screen, armor_bg, (ab_x, y, bar_w, bar_h))
        max_armor = max(player.armor, 1)
        if player.armor > 0:
            fill_w = int(bar_w * (player.armor / max_armor))
            pygame.draw.rect(self.screen, armor_fill, (ab_x, y, fill_w, bar_h))
        pygame.draw.rect(self.screen, BLACK, (ab_x, y, bar_w, bar_h), 2)
        armor_text = self.font.render(f"Armor {player.armor}", True, TEXT_COLOR)
        self.screen.blit(armor_text, (ab_x + 6, y + 2))

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
            self.screen.blit(line_surface, (x, y + i * 22)) 

    
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