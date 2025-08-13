"""
Base Card class and card definitions
"""

# ============================================================================
# CARD DEFINITIONS 
# ============================================================================

CARD_DEFINITIONS = {
    # ========== PLAYER CARDS ==========
    "Slash": {
        "type": "attack",
        "cost": 2,
        "damage": 8,
        "description": "Deal 8 damage",
        "flavor_text": "' Aim the pointy end at the enemy and swing. It's not that hard.'"
    },
    "Kick": {
        "type": "attack",
        "cost": 1,
        "damage": 5,
        "description": "Deal 5 damage",
        "flavor_text": "' I bet you were looking for a joke...I'm sorry but I could not think of anything punny.'"
    },
    "Healing": {
        "type": "utility",
        "cost": 3,
        "effect_type": "heal",
        "effect_value": 10,
        "description": "Heal 10 health",
        "flavor_text": "' Introducing the NEW flavor, never done before...RED.'"
    },
    "Shield": {
        "type": "enhancement",
        "cost": 2,
        "effect_type": "shield",
        "effect_value": 8,
        "description": "Gain 8 armor",
        "flavor_text": "' Who ever said 'math is for blockers', clearly never heard of a shield.'"
    },
    
    # ========== ENEMY CARDS ==========
    "": {
        "type": "attack",
        "cost": 0,
        "damage": 6,
        "description": "Deal 6 damage",
        "flavor_text": "' A sticky situation, but not for long.'"
    },
}

# ============================================================================
# CARD CREATION FUNCTION
# ============================================================================

def create_card(card_name):
    """Create a card instance from the card definitions"""
    if card_name not in CARD_DEFINITIONS:
        raise ValueError(f"Unknown card: {card_name}")
    
    card_data = CARD_DEFINITIONS[card_name]
    card_type = card_data["type"]
    
    if card_type == "attack":
        return AttackCard(
            name=card_name,
            cost=card_data["cost"],
            damage=card_data["damage"],
            description=card_data["description"],
            flavor_text=card_data["flavor_text"]
        )
    elif card_type == "utility":
        return UtilityCard(
            name=card_name,
            cost=card_data["cost"],
            description=card_data["description"],
            effect_type=card_data["effect_type"],
            effect_value=card_data["effect_value"],
            flavor_text=card_data["flavor_text"]
        )
    elif card_type == "enhancement":
        return EnhancementCard(
            name=card_name,
            cost=card_data["cost"],
            description=card_data["description"],
            effect_type=card_data["effect_type"],
            effect_value=card_data["effect_value"],
            flavor_text=card_data["flavor_text"]
        )
    else:
        raise ValueError(f"Unknown card type: {card_type}")

# ============================================================================
# CARD CLASSES
# ============================================================================

class Card:
    def __init__(self, name, cost, description, card_type="Attack", flavor_text=""):
        self.name = name
        self.cost = cost
        self.description = description
        self.card_type = card_type
        self.flavor_text = flavor_text
    
    def use(self, caster, target=None):
        """Use the card - to be overridden by specific cards"""
        pass
    
    def can_target(self, target):
        """Check if this card can target the given entity"""
        return True


class AttackCard(Card):
    def __init__(self, name, cost, damage, description=None, flavor_text=""):
        if description is None:
            description = f"Deal {damage} damage"
        super().__init__(name, cost, description, "Attack", flavor_text)
        self.damage = damage
    
    def use(self, caster, target=None):
        if target:
            # Calculate total damage including strength buffs
            total_damage = self.damage + caster.get_buff_value("strength")
            target.take_damage(total_damage)


class HealCard(Card):
    def __init__(self, name, cost, heal_amount, description=None, flavor_text=""):
        if description is None:
            description = f"Heal {heal_amount} health"
        super().__init__(name, cost, description, "Heal", flavor_text)
        self.heal_amount = heal_amount
    
    def use(self, caster, target=None):
        # Heal cards target the caster by default
        caster.heal(self.heal_amount)


class UtilityCard(Card):
    def __init__(self, name, cost, description, effect_type, effect_value, flavor_text=""):
        super().__init__(name, cost, description, "Utility", flavor_text)
        self.effect_type = effect_type  # "heal", etc.
        self.effect_value = effect_value
    
    def use(self, caster, target=None):
        if self.effect_type == "heal":
            # Heal the caster
            caster.heal(self.effect_value)
        elif self.effect_type == "shield":
            # Add armor/shield to caster
            if not hasattr(caster, 'armor'):
                caster.armor = 0
            caster.armor += self.effect_value


class EnhancementCard(Card):
    def __init__(self, name, cost, description, effect_type, effect_value, flavor_text=""):
        super().__init__(name, cost, description, "Enhancement", flavor_text)
        self.effect_type = effect_type  # "shield", etc.
        self.effect_value = effect_value
    
    def use(self, caster, target=None):
        if self.effect_type == "shield":
            # Add armor/shield to caster
            if not hasattr(caster, 'armor'):
                caster.armor = 0
            caster.armor += self.effect_value
