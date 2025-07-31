"""
Battle State - Manages turn-based combat
"""

from entities.player import Player
from entities.enemy import Enemy
from systems.turn_manager import TurnManager
from cards.deck import Deck

class BattleState:
    def __init__(self):
        # Initialize player and enemy
        self.player = Player()
        self.enemy = Enemy("Green Slime")
        
        # Turn management
        self.turn_manager = TurnManager(self.player, self.enemy)
        
        # Battle state
        self.battle_over = False
        self.winner = None
        
        # Selected card for info display
        self.selected_card_index = None
        self.selected_card_info = None
    
    def handle_input(self, input_handler):
        """Handle input during battle"""
        # Handle double clicks first (for card activation)
        if input_handler.is_mouse_double_clicked():
            mouse_x, mouse_y = input_handler.get_mouse_pos()
            
            # Check if double-clicked on a card
            card_index = self._get_clicked_card(mouse_x, mouse_y)
            if card_index is not None and self.turn_manager.is_player_turn():
                self._activate_card(card_index)
        
        # Handle single clicks (for selection and other actions)
        elif input_handler.is_mouse_clicked():
            mouse_x, mouse_y = input_handler.get_mouse_pos()
            
            # Check if clicked on END TURN button
            if self._is_end_turn_button_clicked(mouse_x, mouse_y) and self.turn_manager.is_player_turn():
                self._end_player_turn()
            
            # Check if clicked on a card (for selection/info display)
            else:
                card_index = self._get_clicked_card(mouse_x, mouse_y)
                if card_index is not None:
                    self._select_card_for_info(card_index)
                else:
                    # Clicked somewhere else, clear selection
                    self.selected_card_index = None
                    self.selected_card_info = None
    
    def update(self):
        """Update battle logic"""
        if not self.battle_over:
            self.turn_manager.update()
            
            # Check for battle end conditions
            if self.player.health <= 0:
                self.battle_over = True
                self.winner = "enemy"
            elif self.enemy.health <= 0:
                self.battle_over = True
                self.winner = "player"
    
    def _get_clicked_card(self, mouse_x, mouse_y):
        """Determine which card was clicked"""
        from utils.constants import HAND_Y, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, SCREEN_WIDTH
        
        # Calculate card positions
        hand_size = len(self.player.hand)
        if hand_size == 0:
            return None
        
        total_width = hand_size * CARD_WIDTH + (hand_size - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        # Check if click is in the card area
        if mouse_y < HAND_Y or mouse_y > HAND_Y + CARD_HEIGHT:
            return None
        
        for i in range(hand_size):
            card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            if card_x <= mouse_x <= card_x + CARD_WIDTH:
                return i
        
        return None
    
    def _select_card_for_info(self, card_index):
        """Select a card to display its information"""
        if 0 <= card_index < len(self.player.hand):
            self.selected_card_index = card_index
            card = self.player.hand[card_index]
            
            # Store card info for display
            self.selected_card_info = {
                'name': card.name,
                'cost': card.cost,
                'description': card.description,
                'flavor_text': getattr(card, 'flavor_text', ''),
                'type': card.card_type
            }
            
            # Add type-specific info
            if hasattr(card, 'damage'):
                self.selected_card_info['damage'] = card.damage
            if hasattr(card, 'heal_amount'):
                self.selected_card_info['heal_amount'] = card.heal_amount
            if hasattr(card, 'effect_value'):
                self.selected_card_info['effect_value'] = card.effect_value
                self.selected_card_info['effect_type'] = card.effect_type
    
    def _activate_card(self, card_index):
        """Activate a card (double-click action)"""
        if 0 <= card_index < len(self.player.hand) and self.turn_manager.is_player_turn():
            card = self.player.hand[card_index]
            
            # Play the card
            if self.player.can_play_card(card):
                self.player.play_card(card, self.enemy)
                
                # Clear selection since card was used
                if self.selected_card_index == card_index:
                    self.selected_card_index = None
                    self.selected_card_info = None
                
                # Check if player has spent all AP or can't afford any more cards
                if not self.player.has_action_points() or not self.player.can_afford_any_card():
                    self.turn_manager.end_player_turn()
    
    def _is_end_turn_button_clicked(self, mouse_x, mouse_y):
        """Check if the END TURN button was clicked"""
        from utils.constants import END_TURN_X, END_TURN_Y, END_TURN_WIDTH, END_TURN_HEIGHT
        
        # Check if click is within the END TURN button area
        if (END_TURN_X <= mouse_x <= END_TURN_X + END_TURN_WIDTH and 
            END_TURN_Y <= mouse_y <= END_TURN_Y + END_TURN_HEIGHT):
            return True
        return False
    
    def _end_player_turn(self):
        """End the player's turn and switch to enemy"""
        print("Player ended turn manually")  # Debug message
        self.turn_manager.end_player_turn()
    
    def get_current_turn(self):
        """Get whose turn it is"""
        return self.turn_manager.current_turn
