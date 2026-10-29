# ==============================================
# Base Character class for all game entities
# ==============================================

class Character:
    def __init__(self, name, max_health, x, y):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.x = x
        self.y = y
        self.is_alive = True
        
        # New attributes for card system
        self.armor = 0
        self.buffs = {}  # Dictionary of active buffs
    
    # Check if character is alive
    def take_damage(self, amount):
        
        # Armor absorbs damage first
        if self.armor > 0:
            armor_absorbed = min(self.armor, amount)
            self.armor -= armor_absorbed
            amount -= armor_absorbed
        
        # Remaining damage goes to health
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            self.is_alive = False
        
        return amount  # Return actual damage dealt to health

    # Heal by amount, not exceeding max health
    def heal(self, amount):
       
        self.health = min(self.max_health, self.health + amount)
    
    # Get health as a percentage (0.0 to 1.0)
    def get_health_percentage(self):
        
        return self.health / self.max_health if self.max_health > 0 else 0
    
    # Update buff durations and remove expired buffs
    def update_buffs(self):
        
        expired_buffs = []
        for buff_name, buff_data in self.buffs.items():
            buff_data['duration'] -= 1
            if buff_data['duration'] <= 0:
                expired_buffs.append(buff_name)
        
        # Remove expired buffs
        for buff_name in expired_buffs:
            del self.buffs[buff_name]
    
    # Get the current value of a specific buff type
    def get_buff_value(self, buff_type):
        if buff_type in self.buffs:
            return self.buffs[buff_type]['value']
        return 0
