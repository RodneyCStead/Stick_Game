"""
Deck management
"""

from cards.card import AttackCard, HealCard
import random

class Deck:
    def __init__(self):
        self.cards = []
        self._create_starting_deck()
        self.shuffle()
    
    def _create_starting_deck(self):
        """Create the player's starting deck"""
        # Basic attack cards
        for _ in range(5):
            self.cards.append(AttackCard("Strike", 1, 6))
        
        for _ in range(2):
            self.cards.append(AttackCard("Heavy Strike", 2, 12))
        
        # Utility cards
        for _ in range(2):
            self.cards.append(HealCard("Heal", 1, 8))
        
        # Special attack
        self.cards.append(AttackCard("Power Strike", 3, 18))
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def draw_card(self):
        """Draw a card from the top of the deck"""
        if self.cards:
            return self.cards.pop()
        return None
    
    def add_card(self, card):
        """Add a card to the deck"""
        self.cards.append(card)
    
    def is_empty(self):
        """Check if deck is empty"""
        return len(self.cards) == 0
