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
        self._initialize_cards()
    
    # Initialize enemy cards based on enemy type
    def _initialize_cards(self):
        from cards.card import AttackCard, UtilityCard

        if self.enemy_type == "Green Slime":
            self.cards = [
                AttackCard("Glorp", 0, 8, "Powerful-ish yucky attack", "This is what I meant by glorp you up."),
                UtilityCard("Slime Shield", 0, "Gain 4 armor", "The slime jiggles defensively.", "shield", 4)
            ]
        elif self.enemy_type == "Blue Slime":
            self.cards = [
                AttackCard("Blurp", 0, 10, "A damp concussive splash attack."),
                UtilityCard("Icy Film", 0, "Gain 6 armor", "The slime cools and hardens.", "shield", 6)
            ]
        else:
            # Generic fallback
            self.cards = [AttackCard("Smack", 0, 5, "A basic enemy attack.")]

    def take_turn(self, target):
        """Enemy AI - choose and use a card"""
        if self.is_alive and self.cards:
            # Simple AI: randomly choose a card to use
            import random
            chosen_card = random.choice(self.cards)
            
            # Use the card
            if chosen_card.card_type == "Attack":
                chosen_card.use(self, target)
                return f"{self.name} uses {chosen_card.name} for {chosen_card.damage} damage!"
            elif chosen_card.card_type in ["Utility", "Enhancement"]:
                chosen_card.use(self, self)  # Target self for utility/enhancement cards
                if chosen_card.effect_type == "heal":
                    return f"{self.name} uses {chosen_card.name} and heals for {chosen_card.effect_value}!"
                elif chosen_card.effect_type == "shield":
                    return f"{self.name} uses {chosen_card.name} and gains {chosen_card.effect_value} armor!"
            
            return f"{self.name} uses {chosen_card.name}!"
        return ""
    
    def get_intent(self):
        """Get what the enemy plans to do (for UI)"""
        if self.cards:
            # For now, show a general intent. Later this could be more sophisticated
            # to show the actual card they'll use next
            attack_cards = [card for card in self.cards if card.card_type == "Attack"]
            if attack_cards:
                avg_damage = sum(card.damage for card in attack_cards) // len(attack_cards)
                return f"Planning Attack (~{avg_damage})"
            else:
                return "Planning Action"
        return "Thinking..."
    
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
