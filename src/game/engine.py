# ======================================================
# Game Engine - Main game loop and state management 
# ======================================================

import pygame
from utils.constants import *
from utils.input_handler import InputHandler
from game.battle import BattleState
from ui.renderer import Renderer

class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.input_handler = InputHandler()
        self.renderer = Renderer(screen)
        
        # Game states
        self.current_state = "battle"  # Start in battle state
        self.battle_state = BattleState()
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        """Handle pygame events"""
        self.input_handler.update(event)
        
        # Pass events to current game state
        if self.current_state == "battle":
            self.battle_state.handle_input(self.input_handler)
    
    def update(self):
        """Update game logic"""
        if self.current_state == "battle":
            self.battle_state.update()
        
        # Reset per-frame input
        self.input_handler.reset_frame()
    
    def update_screen(self, new_screen):
        """Update the screen reference when switching between windowed/fullscreen"""
        self.screen = new_screen
        self.renderer.update_screen(new_screen)  # Use the renderer's update method
        
        # Update the battle state's renderer reference
        if hasattr(self.battle_state, 'renderer'):
            self.battle_state.renderer = self.renderer
        
        # Update character positions for new screen size
        if hasattr(self.battle_state, 'update_character_positions'):
            self.battle_state.update_character_positions()
    
    def render(self):
        """Render the current game state"""
        # Clear screen
        self.screen.fill(BLACK)
        
        if self.current_state == "battle":
            self.renderer.render_battle(self.battle_state)
        
        # Always render FPS counter (for debugging)
        self._render_debug_info()
    
    def _render_debug_info(self):
        """Render debug information"""
        # You can add debug info here
        pass
