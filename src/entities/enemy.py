# ==============================================
# Enemy Character class
# ==============================================

from entities.character import Character
from utils.constants import ENEMY_X, ENEMY_Y
import random

class Enemy(Character):
    def __init__(self, enemy_type="Green Slime"):
        # Expanded enemy stats for multiple enemy types
        enemy_stats = {
            "Green Slime": {
                "health": 60,
                "flavor_text": "Don't be fooled by this creature, it WILL Glorp you up."
            },
            "Blue Slime": {
                "health": 70,
                "flavor_text": "A chillier cousin that packs a wetter punch."
            }
        }

        stats = enemy_stats.get(enemy_type, enemy_stats["Green Slime"])
        super().__init__(enemy_type, stats["health"], ENEMY_X, ENEMY_Y)

        self.enemy_type = enemy_type
        self.flavor_text = stats["flavor_text"]
        self.cards = []  # Enemy's available cards
        self.planned_card = None
        self._initialize_cards()
        self.prepare_intent()
    
    # Initialize enemy cards based on enemy type
    def _initialize_cards(self):
        from cards.card import AttackCard, UtilityCard

        if self.enemy_type == "Green Slime":
            self.cards = [
                AttackCard("Glorp", 0, 8, "A attack the way it sounds when it hits you.")
            ]
        elif self.enemy_type == "Blue Slime":
            self.cards = [
                AttackCard("Blorp", 0, 10, "Like glorp, just blue."),
                UtilityCard("Slime Shield", 0, "Gain 6 armor", "The slime takes shape as poor Bobs shield inside of its body.", "shield", 6)
            ]
        else:
            # Generic fallback
            self.cards = [AttackCard("Smack", 0, 5, "A basic enemy attack.")]

    def prepare_intent(self):
        """Choose the card this enemy will use on its next turn."""
        if self.cards:
            self.planned_card = random.choice(self.cards)
        return self.planned_card

    def take_turn(self, target):
        """Use the card already shown in the enemy intent."""
        if self.is_alive and self.cards:
            chosen_card = self.planned_card or random.choice(self.cards)

            if chosen_card.card_type == "Attack":
                chosen_card.use(self, target)
                message = f"{self.name} uses {chosen_card.name} for {chosen_card.damage} damage!"
            elif chosen_card.card_type in ["Utility", "Enhancement"]:
                chosen_card.use(self, self)
                if chosen_card.effect_type == "heal":
                    message = f"{self.name} uses {chosen_card.name} and heals for {chosen_card.effect_value}!"
                elif chosen_card.effect_type == "shield":
                    message = f"{self.name} uses {chosen_card.name} and gains {chosen_card.effect_value} armor!"
                else:
                    message = f"{self.name} uses {chosen_card.name}!"
            else:
                message = f"{self.name} uses {chosen_card.name}!"

            self.prepare_intent()
            return message
        return ""

    def get_intent(self):
        """Get the card this enemy has planned for its next turn."""
        if self.planned_card is None:
            self.prepare_intent()
        if self.planned_card is None:
            return "Thinking..."

        card = self.planned_card
        if card.card_type == "Attack":
            return f"Attack: {card.name} - {card.damage} damage"
        if getattr(card, "effect_type", None) == "shield":
            return f"Shield: {card.name} - {card.effect_value} armor"
        if getattr(card, "effect_type", None) == "heal":
            return f"Heal: {card.name} ({card.effect_value} health)"
        return f"Action: {card.name}"
    
    def get_card_info(self, card_name):
        """Get detailed information about a specific card"""
        for card in self.cards:
            if card.name == card_name:
                return {
                    'name': card.name,
                    'description': card.description,
                    'flavor_text': card.flavor_text,
                    'type': card.card_type
                }
        return None
    
    def list_all_cards(self):
        """List all cards with their flavor text - useful for debugging/testing"""
        card_info = []
        for card in self.cards:
            card_info.append({
                'name': card.name,
                'description': card.description,
                'flavor_text': card.flavor_text,
                'type': card.card_type
            })
        return card_info
