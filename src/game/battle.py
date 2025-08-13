# ==============================================
# Battle State Management
# ==============================================

from entities.player import Player
from entities.enemy import Enemy
from systems.turn_manager import TurnManager
from cards.deck import Deck
from utils.animation_manager import animation_manager

class BattleState:

    # Initialize a battle instance (supports multiple enemies).
    def __init__(self, player=None, enemies=None):
        self.player = player if player else Player()

        # Enemy list
        if enemies is None:
            enemies = [Enemy("Green Slime")]
        self.enemies = enemies

        # Primary enemy (first alive)
        self.enemy = self._get_primary_enemy()

        # Turn manager (multi-enemy aware)
        self.turn_manager = TurnManager(self.player, self.enemy, enemies_list=self.enemies)

        # Battle state flags
        self.battle_over = False
        self.winner = None

        # UI selection state
        self.selected_card_index = None
        self.selected_card_info = None
        self.selected_enemy = None  # Enemy selection (targeting/info)

        # Pending delayed effects (list of dicts with execute_after timestamp and callable)
        self._pending_effects = []

        # Layout enemies
        self._layout_enemy_positions()

    # Update character positions
    def update_character_positions(self):
        from utils.constants import PLAYER_X, CHARACTER_Y
        # Update player position (X fixed, Y fixed for now)
        self.player.x = PLAYER_X
        self.player.y = CHARACTER_Y
        # Re-layout enemies (responsive to screen changes)
        self._layout_enemy_positions()

    # Layout enemy positions
    def _layout_enemy_positions(self):
        from utils.constants import ENEMY_X, ENEMY_Y
        if not self.enemies:
            return
        count = len(self.enemies)
        if count == 1:
            e = self.enemies[0]
            e.x = ENEMY_X
            e.y = ENEMY_Y
            return
        # Spacing between enemy centers
        spacing = 160
        # Center group around ENEMY_X
        total_width = (count - 1) * spacing
        start_x = ENEMY_X - total_width / 2
        for idx, enemy in enumerate(self.enemies):
            enemy.x = int(start_x + idx * spacing)
            enemy.y = ENEMY_Y

    # Handle user input
    def handle_input(self, input_handler):
        
        # Don't allow input during animations
        if animation_manager.is_animation_active():
            return
            
        # Handle double clicks first (for card activation)
        if input_handler.is_mouse_double_clicked():
            mouse_x, mouse_y = input_handler.get_mouse_pos()
            
            # Check if double-clicked on a card
            card_index = self._get_clicked_card(mouse_x, mouse_y)
            if card_index is not None and self.turn_manager.is_player_turn():
                self._activate_card(card_index)
        
        # Handle single clicks (for selection and other actions)
        elif input_handler.is_mouse_clicked():
            mouse_x, mouse_y = input_handler.get_mouse_pos()
            
            # Check if clicked on END TURN button
            if self._is_end_turn_button_clicked(mouse_x, mouse_y) and self.turn_manager.is_player_turn():
                self._end_player_turn()
            
            # Check if clicked on a card (for selection/info display)
            else:
                # Check if clicked on an enemy first (selection / targeting)
                enemy_clicked = self._get_clicked_enemy(mouse_x, mouse_y)
                if enemy_clicked:
                    self.selected_enemy = enemy_clicked
                    # Clear card selection (panel will show enemy info)
                    self.selected_card_index = None
                    self.selected_card_info = None
                else:
                    # Check for card selection
                    card_index = self._get_clicked_card(mouse_x, mouse_y)
                    if card_index is not None:
                        # Keep existing enemy target when selecting a card so player can view card info AND keep target
                        self._select_card_for_info(card_index)
                    else:
                        # Clicked somewhere else, clear selections
                        self.selected_card_index = None
                        self.selected_card_info = None
                        self.selected_enemy = None

    # Update battle logic
    def update(self):
        
        if not self.battle_over:
            self.turn_manager.update()

            # Resolve any pending delayed card effects whose time has come
            import time
            now = time.time()
            if self._pending_effects:
                remaining = []
                for eff in self._pending_effects:
                    if now >= eff['execute_after']:
                        try:
                            eff['func']()
                        except Exception as e:
                            print('[BattleState][ERROR] executing delayed effect', e)
                    else:
                        remaining.append(eff)
                self._pending_effects = remaining

            # Update primary enemy reference to first alive
            self.enemy = self._get_primary_enemy()

            # Clear selected enemy if it died
            if self.selected_enemy and not self.selected_enemy.is_alive:
                self.selected_enemy = None

            # Battle end conditions
            if self.player.health <= 0:
                self.battle_over = True
                self.winner = "enemy"
            elif all(not e.is_alive for e in self.enemies):
                self.battle_over = True
                self.winner = "player"

    # Get the primary enemy (first alive)
    def _get_primary_enemy(self):
        for e in getattr(self, 'enemies', []):
            if e.is_alive:
                return e
        return self.enemies[0] if getattr(self, 'enemies', []) else None

    # Get all active enemies
    def get_active_enemies(self):
        return [e for e in self.enemies if e.is_alive]

    # Get the card that was clicked
    def _get_clicked_card(self, mouse_x, mouse_y):
        from utils.constants import HAND_Y, CARD_WIDTH, CARD_HEIGHT, CARD_SPACING, SCREEN_WIDTH
        
        # Calculate card positions
        hand_size = len(self.player.hand)
        if hand_size == 0:
            return None
        
        total_width = hand_size * CARD_WIDTH + (hand_size - 1) * CARD_SPACING
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        # Check if click is in the card area
        if mouse_y < HAND_Y or mouse_y > HAND_Y + CARD_HEIGHT:
            return None
        
        for i in range(hand_size):
            card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            if card_x <= mouse_x <= card_x + CARD_WIDTH:
                return i
        
        return None

    # Get the enemy that was clicked
    def _get_clicked_enemy(self, mouse_x, mouse_y):
        
        width, height = 140, 160
        for enemy in self.get_active_enemies():
            ex, ey = enemy.x, enemy.y
            left = ex - width // 2
            top = ey - height // 2
            if left <= mouse_x <= left + width and top <= mouse_y <= top + height:
                return enemy
        return None
    
    def _select_card_for_info(self, card_index):
        """Select a card to display its information"""
        if 0 <= card_index < len(self.player.hand):
            self.selected_card_index = card_index
            card = self.player.hand[card_index]
            
            # Store card info for display
            self.selected_card_info = {
                'name': card.name,
                'cost': card.cost,
                'description': card.description,
                'flavor_text': getattr(card, 'flavor_text', ''),
                'type': card.card_type
            }
            
            # Add type-specific info
            if hasattr(card, 'damage'):
                self.selected_card_info['damage'] = card.damage
            if hasattr(card, 'heal_amount'):
                self.selected_card_info['heal_amount'] = card.heal_amount
            if hasattr(card, 'effect_value'):
                self.selected_card_info['effect_value'] = card.effect_value
                self.selected_card_info['effect_type'] = card.effect_type
    
    def _activate_card(self, card_index):
        """Activate a card (double-click action)"""
        if 0 <= card_index < len(self.player.hand) and self.turn_manager.is_player_turn():
            card = self.player.hand[card_index]
            
            # Play the card
            if self.player.can_play_card(card):
                # Start animation (get duration)
                # Determine target: selected enemy if alive else primary
                target_enemy = self.selected_enemy if (self.selected_enemy and self.selected_enemy.is_alive) else self.enemy
                duration = animation_manager.start_card_animation(card.name, self.player, target_enemy)

                # Pay cost & move card to discard immediately, but defer effect if attack
                self.player.action_points -= card.cost
                from cards.card import AttackCard
                if isinstance(card, AttackCard) and target_enemy and target_enemy.is_alive:
                    import time
                    damage = card.damage + self.player.get_buff_value("strength")
                    def apply_damage(target_ref=target_enemy, dmg=damage):
                        if target_ref.is_alive:
                            target_ref.take_damage(dmg)
                    self._pending_effects.append({
                        'execute_after': time.time() + duration,
                        'func': apply_damage
                    })
                else:
                    # Immediate resolution for non-attack or no enemy
                    card.use(self.player, target_enemy)

                # Discard card
                if card in self.player.hand:
                    self.player.hand.remove(card)
                    self.player.discard_pile.append(card)
                
                # Clear selection since card was used
                if self.selected_card_index == card_index:
                    self.selected_card_index = None
                    self.selected_card_info = None
                
                # Check if player has spent all AP or can't afford any more cards
                if not self.player.has_action_points() or not self.player.can_afford_any_card():
                    self.turn_manager.end_player_turn()

    # Check if the END TURN button was clicked
    def _is_end_turn_button_clicked(self, mouse_x, mouse_y):
        
        from utils.constants import END_TURN_X, END_TURN_Y, END_TURN_WIDTH, END_TURN_HEIGHT
        
        # Check if click is within the END TURN button area
        if (END_TURN_X <= mouse_x <= END_TURN_X + END_TURN_WIDTH and 
            END_TURN_Y <= mouse_y <= END_TURN_Y + END_TURN_HEIGHT):
            return True
        return False
    
    def _end_player_turn(self):
        """End the player's turn and switch to enemy"""
        self.turn_manager.end_player_turn()
    
    def get_current_turn(self):
        """Get whose turn it is"""
        return self.turn_manager.current_turn
