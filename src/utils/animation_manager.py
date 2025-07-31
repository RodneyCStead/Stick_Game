"""
Animation Manager - Handles character animations and timing
"""

import pygame
import time

class AnimationManager:
    def __init__(self):
        self.current_animations = {}  # Track active animations
        self.animation_queue = []     # Queue of animations to play
        
    def start_card_animation(self, card_name, caster, target=None):
        """Start animation sequence for a specific card"""
        if card_name.lower() == "slash":
            self._start_slash_animation(caster, target)
    
    def _start_slash_animation(self, player, enemy):
        """Start the slash animation sequence"""
        current_time = time.time()
        
        # Define the animation sequence
        animation_sequence = [
            {
                'character': 'player',
                'state': 'Slash_1',
                'start_time': current_time,
                'duration': 2.0  # 2 seconds
            },
            {
                'character': 'player', 
                'state': 'Slash_2',
                'start_time': current_time + 2.0,
                'duration': 2.0  # 2 seconds
            },
            {
                'character': 'enemy',
                'state': 'Slashed', 
                'start_time': current_time + 4.0,  # When player reaches Slash_2
                'duration': 1.0  # 1 second
            },
            {
                'character': 'both',
                'state': 'idle',
                'start_time': current_time + 5.0,  # Return to idle
                'duration': 0.0  # Permanent until next animation
            }
        ]
        
        # Store the animation sequence
        self.animation_queue = animation_sequence
        self.current_animations['slash'] = {
            'active': True,
            'start_time': current_time,
            'total_duration': 5.0
        }
    
    def get_character_state(self, character_type):
        """Get the current animation state for a character"""
        current_time = time.time()
        
        # Check if any animations are active
        for anim in self.animation_queue:
            if current_time >= anim['start_time'] and current_time < anim['start_time'] + anim['duration']:
                if anim['character'] == character_type or anim['character'] == 'both':
                    return anim['state']
        
        # Default to idle if no animation is active
        return 'idle'
    
    def is_animation_active(self):
        """Check if any animation is currently playing"""
        current_time = time.time()
        
        for anim_name, anim_data in self.current_animations.items():
            if anim_data['active']:
                if current_time < anim_data['start_time'] + anim_data['total_duration']:
                    return True
                else:
                    # Animation finished, mark as inactive
                    anim_data['active'] = False
        
        return False
    
    def update(self):
        """Update animation system - call this every frame"""
        current_time = time.time()
        
        # Clean up finished animations
        for anim_name in list(self.current_animations.keys()):
            anim_data = self.current_animations[anim_name]
            if anim_data['active'] and current_time >= anim_data['start_time'] + anim_data['total_duration']:
                anim_data['active'] = False
                self.animation_queue.clear()  # Clear the queue when animation finishes

# Global animation manager instance
animation_manager = AnimationManager()
