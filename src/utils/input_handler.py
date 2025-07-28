"""
Input handling utilities
"""

import pygame

class InputHandler:
    def __init__(self):
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.keys_pressed = set()
    
    def update(self, event):
        """Update input state based on pygame event"""
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.mouse_clicked = True
                self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_clicked = False
        elif event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            self.keys_pressed.discard(event.key)
    
    def is_key_pressed(self, key):
        """Check if a key is currently pressed"""
        return key in self.keys_pressed
    
    def get_mouse_pos(self):
        """Get current mouse position"""
        return self.mouse_pos
    
    def is_mouse_clicked(self):
        """Check if mouse was clicked this frame"""
        return self.mouse_clicked
    
    def reset_frame(self):
        """Reset per-frame input states"""
        self.mouse_clicked = False
