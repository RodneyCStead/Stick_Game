"""
Deck management
"""

from cards.card import AttackCard, HealCard, UtilityCard, EnhancementCard
import random

class Deck:
    def __init__(self):
        self.cards = []
        self._create_starting_deck()
        self.shuffle()
    
    def _create_starting_deck(self):
        """Create the player's starting deck with 10 cards total"""
        
        # ATTACK CARDS - Slash
        for _ in range(4):
            self.cards.append(AttackCard("Slash", 2, 8))
        
        # ATTACK CARDS - Kick 
        for _ in range(2):
            self.cards.append(AttackCard("Kick", 1, 5))
        
        # UTILITY CARD - Healing Potion (1 card)
        for _ in range(1):
            self.cards.append(UtilityCard("Healing", 2, "Heal 10 health", "heal", 10))
        
        # ENHANCEMENT CARD - Shield (3 cards)
        for _ in range(3):
            self.cards.append(EnhancementCard("Shield", 2, "Gain 8 armor", "shield", 8))
    
    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self.cards)
    
    def draw_card(self):
        """Draw a card from the top of the deck, reshuffling discard if needed"""
        if not self.cards:
            # Deck is empty, need to reshuffle discard pile
            return None  # Player will handle reshuffling from discard pile
        return self.cards.pop()
    
    def reshuffle_from_discard(self, discard_pile):
        """Reshuffle discard pile back into deck"""
        if discard_pile:
            self.cards.extend(discard_pile)
            discard_pile.clear()
            self.shuffle()
            print(f"Deck reshuffled! Now has {len(self.cards)} cards")
    
    def cards_remaining(self):
        """Get number of cards remaining in deck"""
        return len(self.cards)
    
    def add_card(self, card):
        """Add a card to the deck"""
        self.cards.append(card)
    
    def is_empty(self):
        """Check if deck is empty"""
        return len(self.cards) == 0
