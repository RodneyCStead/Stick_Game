"""
Player Character class
"""

from entities.character import Character
from cards.deck import Deck
from utils.constants import PLAYER_X, CHARACTER_Y

class Player(Character):
    def __init__(self):
        super().__init__("Player", 100, PLAYER_X, CHARACTER_Y)
        
        # Player-specific attributes
        self.mana = 3
        self.max_mana = 3
        self.deck = Deck()
        self.hand = []
        self.discard_pile = []
        
        # Draw initial hand
        self.draw_hand()
    
    def draw_hand(self, hand_size=5):
        """Draw cards from deck to hand"""
        cards_to_draw = min(hand_size - len(self.hand), len(self.deck.cards))
        
        for _ in range(cards_to_draw):
            if self.deck.cards:
                card = self.deck.draw_card()
                self.hand.append(card)
    
    def can_play_card(self, card):
        """Check if player can play this card"""
        return self.mana >= card.cost
    
    def play_card(self, card, target=None):
        """Play a card from hand"""
        if self.can_play_card(card):
            # Pay mana cost
            self.mana -= card.cost
            
            # Execute card effect
            card.use(self, target)
            
            # Move card to discard pile
            if card in self.hand:
                self.hand.remove(card)
                self.discard_pile.append(card)
            
            return True
        return False
    
    def start_turn(self):
        """Actions at start of player turn"""
        # Restore mana
        self.mana = self.max_mana
        
        # Draw a card
        if len(self.hand) < 7:  # Hand size limit
            self.draw_hand(len(self.hand) + 1)
    
    def end_turn(self):
        """Actions at end of player turn"""
        pass
