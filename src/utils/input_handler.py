"""
Input handling utilities
"""

import pygame

class InputHandler:
    def __init__(self):
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.mouse_double_clicked = False
        self.last_click_time = 0
        self.double_click_threshold = 0.5  # 500ms for double click
        self.keys_pressed = set()
    
    def update(self, event):
        """Update input state based on pygame event"""
        import time
        
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                current_time = time.time()
                
                # Check for double click
                if current_time - self.last_click_time < self.double_click_threshold:
                    self.mouse_double_clicked = True
                    self.mouse_clicked = False  
                else:
                    self.mouse_clicked = True
                    self.mouse_double_clicked = False
                
                self.last_click_time = current_time
                self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pass  
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
    
    def is_mouse_double_clicked(self):
        """Check if mouse was double clicked this frame"""
        return self.mouse_double_clicked
    
    def reset_frame(self):
        """Reset per-frame input states"""
        self.mouse_clicked = False
        self.mouse_double_clicked = False
