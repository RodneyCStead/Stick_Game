# ==============================================
# Turn Manager - Handles turn-based combat logic    
# ==============================================

from utils.animation_manager import animation_manager

class TurnManager:
    def __init__(self, player, enemy, enemies_list=None):
        self.player = player
        self.enemy = enemy  # primary enemy (backwards compatibility)
        # Optional list of enemies for multi-enemy battles
        self.enemies_list = enemies_list if enemies_list else [enemy]
        self.current_turn = "player"  # "player" or "enemy"
        self.turn_count = 1
        self._enemy_index = 0  # index for cycling through multiple enemies

        # Start the first turn
        self.start_player_turn()
    
    def is_player_turn(self):
        """Check if it's the player's turn"""
        return self.current_turn == "player"
    
    def is_enemy_turn(self):
        """Check if it's the enemy's turn"""
        return self.current_turn == "enemy"
    
    def start_player_turn(self):
        """Start the player's turn"""
        self.current_turn = "player"
        self.player.start_turn()
    
    def end_player_turn(self):
        """End the player's turn and start enemy turn"""
        # Don't end turn if animations are playing
        if animation_manager.is_animation_active():
            return
            
        self.player.end_turn()
        self.current_turn = "enemy"
        self.start_enemy_turn()
    
    def start_enemy_turn(self):
        """Start the enemy turn (supports multiple enemies)."""
        # Skip dead enemies
        alive_enemies = [e for e in self.enemies_list if e.is_alive]
        if not alive_enemies:
            # No enemies alive; player wins handled elsewhere
            self.end_enemy_turn()
            return

        # Pick current enemy by index
        if self._enemy_index >= len(alive_enemies):
            self._enemy_index = 0
        acting_enemy = alive_enemies[self._enemy_index]
        self.enemy = acting_enemy  # update primary reference for compatibility

        # Enemy acts
        acting_enemy.take_turn(self.player)

        # Prepare next enemy for next enemy phase (if we extend to per-enemy turns)
        self._enemy_index += 1
        # For now, end enemy turn after single enemy acts (simple model)
        self.end_enemy_turn()
    
    def end_enemy_turn(self):
        """End the enemy's turn and start next player turn"""
        self.turn_count += 1
        self.start_player_turn()
    
    def update(self):
        """Update turn logic - check if animations finished"""
        # If we're waiting for animations to finish before switching turns
        if self.current_turn == "enemy" and not animation_manager.is_animation_active():
            # Animation finished, can proceed with turn logic
            pass
