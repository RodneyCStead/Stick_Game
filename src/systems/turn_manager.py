# ==============================================
# Turn Manager - Handles turn-based combat logic    
# ==============================================

from utils.animation_manager import animation_manager

class TurnManager:
    def __init__(self, player, enemy, enemies_list=None):
        self.player = player
        self.enemy = enemy  
        self.enemies_list = enemies_list if enemies_list else [enemy]
        self.current_turn = "player"  
        self.turn_count = 1
        self._enemy_index = 0

        # Start the first turn
        self.start_player_turn()
    
    def is_player_turn(self):
        """Check if it's the player's turn"""
        return self.current_turn == "player"

    # Check if it's the enemy's turn
    def is_enemy_turn(self):
        return self.current_turn == "enemy"

    # Start the player's turn
    def start_player_turn(self):
        self.current_turn = "player"
        self.player.start_turn()

    # End the player's turn and checks if animations are playing, if so it wont end
    def end_player_turn(self):
     
        if animation_manager.is_animation_active():
            return
            
        self.player.end_turn()
        self.current_turn = "enemy"
        self.start_enemy_turn()
    
    # This function makes each living enemy take their turn to attack the player, one at a time.
    def start_enemy_turn(self):
        
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
        self.enemy = acting_enemy  


        # Enemy takes turn
        acting_enemy.take_turn(self.player)

        # Prepare for next enemy 
        self._enemy_index += 1
        self.end_enemy_turn()

    # End the enemy's turn and start next player turn
    def end_enemy_turn(self):
        self.turn_count += 1
        self.start_player_turn()

    # Update turn logic if animations are playing
    def update(self):
        if self.current_turn == "enemy" and not animation_manager.is_animation_active():
            pass
