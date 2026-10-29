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
        elif card_name.lower() == "kick":
            self._start_kick_animation(caster, target)


    # Slash animation sequence
    def _start_slash_animation(self, player, enemy):
        """Start the slash animation sequence"""
        current_time = time.time()
        
        animation_sequence = [
            {
                'character': 'player',
                'state': 'Slash_1',
                'start_time': current_time,
                'duration': 1.5  
            },
            {
                'character': 'player', 
                'state': 'Slash_2',
                'start_time': current_time + 1.5,
                'duration': 1.5  
            },
            {
                'character': 'enemy',
                'state': 'Slashed', 
                'start_time': current_time + 3.0,
                'duration': 1.5
            },
            {
                'character': 'both',
                'state': 'idle',
                'start_time': current_time + 4.5,  
                'duration': 0.0  
            }
        ]
        
        
        self.animation_queue = animation_sequence
        self.current_animations['slash'] = {
            'active': True,
            'start_time': current_time,
            'total_duration': 4.5
        }
        
    def _start_kick_animation(self,player,enemy):

        current_time = time.time()
        
        animation_sequence = [
            {
                'character': 'player',
                'state': 'Kick_1',
                'start_time': current_time,
                'duration': 1.5
            },
            {
                'character': 'player',
                'state': 'Kick_2',
                'start_time': current_time + 1.5,
                'duration': 1.5
            },{
                'character': 'enemy',
                'state': 'Kicked',
                'start_time': current_time + 3.0,
                'duration': 1.5
            },{
                'character': 'both',
                'state': 'idle',
                'start_time': current_time + 4.5,
                'duration': 0.0
            }
        ]
        
        self.animation_queue = animation_sequence
        self.current_animations['kick'] = {
            'active': True,
            'start_time': current_time,
            'total_duration': 4.5
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
