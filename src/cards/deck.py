"""
Deck management
"""

from cards.card import create_card
import random

# ============================================================================
# STARTER DECK CONFIGURATION
# ============================================================================

STARTER_DECK_COMPOSITION = {
    "Slash": 4,     
    "Kick": 2,       
    "Healing": 1, 
    "Shield": 3     
}

class Deck:
    def __init__(self):
        self.cards = []
        self._create_starting_deck()
        self.shuffle()
    
    def _create_starting_deck(self):
        """Create the player's starting deck using the composition defined above"""
        for card_name, count in STARTER_DECK_COMPOSITION.items():
            for _ in range(count):
                self.cards.append(create_card(card_name))

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
