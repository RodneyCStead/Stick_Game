"""
Deck management
"""

from cards.card import AttackCard, HealCard, UtilityCard, BuffCard
import random

class Deck:
    def __init__(self):
        self.cards = []
        self._create_starting_deck()
        self.shuffle()
    
    def _create_starting_deck(self):
        """Create the player's starting deck with 4 card types"""
        
        # ATTACK CARDS (2 types)
        for _ in range(3):
            self.cards.append(AttackCard("Slash", 1, 8))
        
        for _ in range(3):
            self.cards.append(AttackCard("Kick", 1, 6))
        
        # UTILITY CARD (1 type)
        for _ in range(3):
            self.cards.append(UtilityCard("Healing", 1, "Heal 10 health", "heal", 10))
        
        # ENHANCEMENT CARD (1 type)
        for _ in range(3):
            self.cards.append(UtilityCard("Shield", 2, "Gain 8 armor", "shield", 8))
    
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
