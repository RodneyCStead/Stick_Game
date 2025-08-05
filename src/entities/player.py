# ==============================================
# Player Character class    
# ==============================================

from entities.character import Character
from cards.deck import Deck
from utils.constants import PLAYER_X, CHARACTER_Y

class Player(Character):
    def __init__(self):
        super().__init__("Player", 100, PLAYER_X, CHARACTER_Y)
        
        # Player-specific attributes
        self.action_points = 5  # Changed from mana to action points
        self.max_action_points = 5
        self.deck = Deck()
        self.hand = []
        self.discard_pile = []
        
        # Draw initial hand (4 cards)
        self.draw_hand(4)
    
    def draw_hand(self, target_hand_size=4):
        """Draw cards from deck to reach target hand size (default 4)"""
        cards_to_draw = target_hand_size - len(self.hand)
        
        for _ in range(cards_to_draw):
            card = self.draw_single_card()
            if card:
                self.hand.append(card)
    
    def draw_single_card(self):
        """Draw a single card, handling deck reshuffling"""
        card = self.deck.draw_card()
        
        # If deck is empty, try to reshuffle discard pile
        if card is None and self.discard_pile:
            print("Deck empty! Reshuffling discard pile...")
            self.deck.reshuffle_from_discard(self.discard_pile)
            card = self.deck.draw_card()
        
        return card
    
    def can_play_card(self, card):
        """Check if player can play this card"""
        return self.action_points >= card.cost
    
    def play_card(self, card, target=None):
        """Play a card from hand"""
        if self.can_play_card(card):
            # Pay action point cost
            self.action_points -= card.cost
            
            # Execute card effect
            card.use(self, target)
            
            # Move card to discard pile
            if card in self.hand:
                self.hand.remove(card)
                self.discard_pile.append(card)
            
            return True
        return False
    
    def has_action_points(self):
        """Check if player has any action points left"""
        return self.action_points > 0
    
    def can_afford_any_card(self):
        """Check if player can afford to play any card in hand"""
        return any(self.can_play_card(card) for card in self.hand)

    # Actions at start of player turn
    def start_turn(self):
        
        # Update buffs (reduce duration)
        self.update_buffs()
        
        # Restore action points
        self.action_points = self.max_action_points
        
        # Draw back to 4 cards if hand is below 4
        if len(self.hand) < 4:
            self.draw_hand(4)
    
    # Actions at end of player turn
    def end_turn(self):
        pass
