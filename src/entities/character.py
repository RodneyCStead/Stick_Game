"""
Base Character class for all game entities
"""

class Character:
    def __init__(self, name, max_health, x, y):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.x = x
        self.y = y
        self.is_alive = True
    
    def take_damage(self, amount):
        """Take damage and update alive status"""
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.is_alive = False
    
    def heal(self, amount):
        """Heal by amount, not exceeding max health"""
        self.health = min(self.max_health, self.health + amount)
    
    def get_health_percentage(self):
        """Get health as a percentage (0.0 to 1.0)"""
        return self.health / self.max_health if self.max_health > 0 else 0
