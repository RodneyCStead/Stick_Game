"""
Base Card class
"""

class Card:
    def __init__(self, name, cost, description, card_type="Attack"):
        self.name = name
        self.cost = cost
        self.description = description
        self.card_type = card_type
    
    def use(self, caster, target=None):
        """Use the card - to be overridden by specific cards"""
        pass
    
    def can_target(self, target):
        """Check if this card can target the given entity"""
        return True


class AttackCard(Card):
    def __init__(self, name, cost, damage, description=None):
        if description is None:
            description = f"Deal {damage} damage"
        super().__init__(name, cost, description, "Attack")
        self.damage = damage
    
    def use(self, caster, target=None):
        if target:
            # Calculate total damage including strength buffs
            total_damage = self.damage + caster.get_buff_value("strength")
            target.take_damage(total_damage)


class HealCard(Card):
    def __init__(self, name, cost, heal_amount, description=None):
        if description is None:
            description = f"Heal {heal_amount} health"
        super().__init__(name, cost, description, "Heal")
        self.heal_amount = heal_amount
    
    def use(self, caster, target=None):
        # Heal cards target the caster by default
        caster.heal(self.heal_amount)


class UtilityCard(Card):
    def __init__(self, name, cost, description, effect_type, effect_value):
        super().__init__(name, cost, description, "Utility")
        self.effect_type = effect_type  # "shield", "heal", etc.
        self.effect_value = effect_value
    
    def use(self, caster, target=None):
        if self.effect_type == "shield":
            # Add armor/shield to caster
            if not hasattr(caster, 'armor'):
                caster.armor = 0
            caster.armor += self.effect_value
        elif self.effect_type == "heal":
            # Heal the caster
            caster.heal(self.effect_value)


class BuffCard(Card):
    def __init__(self, name, cost, description, buff_type, buff_value, duration=3):
        super().__init__(name, cost, description, "Buff")
        self.buff_type = buff_type  # "strength", "speed", etc.
        self.buff_value = buff_value
        self.duration = duration
    
    def use(self, caster, target=None):
        # Add temporary buff to caster
        if not hasattr(caster, 'buffs'):
            caster.buffs = {}
        caster.buffs[self.buff_type] = {
            'value': self.buff_value,
            'duration': self.duration
        }
