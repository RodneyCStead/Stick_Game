"""
Turn Management System
"""

class TurnManager:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.current_turn = "player"  # "player" or "enemy"
        self.turn_count = 1
        
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
        self.player.end_turn()
        self.current_turn = "enemy"
        self.start_enemy_turn()
    
    def start_enemy_turn(self):
        """Start the enemy's turn"""
        if self.enemy.is_alive:
            # Enemy takes their action
            self.enemy.take_turn(self.player)
            
            # End enemy turn after a delay (in a real game, you'd animate this)
            self.end_enemy_turn()
    
    def end_enemy_turn(self):
        """End the enemy's turn and start next player turn"""
        self.turn_count += 1
        self.start_player_turn()
    
    def update(self):
        """Update turn logic"""
        # Handle any turn-based timing or animations here
        pass
