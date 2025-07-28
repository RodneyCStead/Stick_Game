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
        """Create the player's starting deck with all card types"""
        
        # ATTACK CARDS
        for _ in range(4):
            self.cards.append(AttackCard("Strike", 1, 6))
        
        for _ in range(2):
            self.cards.append(AttackCard("Heavy Strike", 2, 12))
        
        self.cards.append(AttackCard("Power Strike", 3, 18))
        
        # UTILITY CARDS
        for _ in range(2):
            self.cards.append(UtilityCard("Shield Block", 1, "Gain 6 armor", "shield", 6))
        
        for _ in range(2):
            self.cards.append(UtilityCard("Healing Potion", 1, "Heal 8 health", "heal", 8))
        
        self.cards.append(UtilityCard("Iron Defense", 2, "Gain 12 armor", "shield", 12))
        
        # BUFF CARDS
        self.cards.append(BuffCard("Rage", 2, "Deal +3 damage for 3 turns", "strength", 3, 3))
        self.cards.append(BuffCard("Focus", 1, "Deal +2 damage for 2 turns", "strength", 2, 2))
    
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
