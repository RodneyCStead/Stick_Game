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
            target.take_damage(self.damage)


class HealCard(Card):
    def __init__(self, name, cost, heal_amount, description=None):
        if description is None:
            description = f"Heal {heal_amount} health"
        super().__init__(name, cost, description, "Heal")
        self.heal_amount = heal_amount
    
    def use(self, caster, target=None):
        # Heal cards target the caster by default
        caster.heal(self.heal_amount)


class BuffCard(Card):
    def __init__(self, name, cost, description):
        super().__init__(name, cost, description, "Buff")
    
    def use(self, caster, target=None):
        # Placeholder for buff effects
        pass
