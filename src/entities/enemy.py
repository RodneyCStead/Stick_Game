"""
Enemy Character class
"""

from entities.character import Character
from utils.constants import ENEMY_X, CHARACTER_Y
import random

class Enemy(Character):
    def __init__(self, enemy_type="Goblin"):
        # Enemy stats based on type
        enemy_stats = {
            "Goblin": {"health": 60, "damage": 8},
            "Orc": {"health": 80, "damage": 12},
            "Troll": {"health": 120, "damage": 15}
        }
        
        stats = enemy_stats.get(enemy_type, enemy_stats["Goblin"])
        super().__init__(enemy_type, stats["health"], ENEMY_X, CHARACTER_Y)
        
        self.damage = stats["damage"]
        self.enemy_type = enemy_type
    
    def take_turn(self, target):
        """Enemy AI - simple attack for now"""
        if self.is_alive:
            # Simple AI: always attack
            damage = random.randint(self.damage - 2, self.damage + 2)
            target.take_damage(damage)
            return f"{self.name} attacks for {damage} damage!"
        return ""
    
    def get_intent(self):
        """Get what the enemy plans to do (for UI)"""
        return f"Attack ({self.damage})"
