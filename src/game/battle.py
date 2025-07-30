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
        self.enemy = Enemy("Goblin")
        
        # Turn management
        self.turn_manager = TurnManager(self.player, self.enemy)
        
        # Battle state
        self.battle_over = False
        self.winner = None
        
        # Selected card
        self.selected_card_index = None
    
    def handle_input(self, input_handler):
        """Handle input during battle"""
        if input_handler.is_mouse_clicked():
            mouse_x, mouse_y = input_handler.get_mouse_pos()
            
            # Check if clicked on a card
            card_index = self._get_clicked_card(mouse_x, mouse_y)
            if card_index is not None and self.turn_manager.is_player_turn():
                self._select_card(card_index)
    
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
    
    def _select_card(self, card_index):
        """Select and play a card"""
        if 0 <= card_index < len(self.player.hand):
            card = self.player.hand[card_index]
            
            # Play the card
            if self.player.can_play_card(card):
                self.player.play_card(card, self.enemy)
                
                # Check if player has spent all AP or can't afford any more cards
                if not self.player.has_action_points() or not self.player.can_afford_any_card():
                    self.turn_manager.end_player_turn()
    
    def get_current_turn(self):
        """Get whose turn it is"""
        return self.turn_manager.current_turn
