"""
Animation Manager - Handles character animations and timing
"""

import pygame
import time

class AnimationManager:
    def __init__(self):
            # Active animation tracking
            self.current_animations = {}
            # Ordered sequence of frame/state changes
            self.animation_queue = []
            # Target enemy for current player attack animation (used to scope enemy hit animation)
            self.current_enemy_target = None
        
    def start_card_animation(self, card_name, caster, target=None):
        """Start animation sequence for a specific card"""
        lowered = card_name.lower()
        if lowered == "slash":
            self.current_enemy_target = target
            return self._start_slash_animation(caster, target)
        elif lowered == "kick":
            self.current_enemy_target = target
            return self._start_kick_animation(caster, target)
        return 0.0  # No animation / instant


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
        total = 4.5
        self.current_animations['slash'] = {
            'active': True,
            'start_time': current_time,
            'total_duration': total
        }
        return total
        
    def _start_kick_animation(self, player, enemy):
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
        total = 4.5
        self.current_animations['kick'] = {
            'active': True,
            'start_time': current_time,
            'total_duration': total
        }
        return total

    def get_total_duration(self, card_name):
        """Return total animation duration for card name if active/known."""
        key = card_name.lower()
        anim_key = 'slash' if key == 'slash' else 'kick' if key == 'kick' else None
        if anim_key and anim_key in self.current_animations:
            return self.current_animations[anim_key].get('total_duration', 0.0)
        return 0.0
    
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
        any_active = False
        for anim_name in list(self.current_animations.keys()):
            anim_data = self.current_animations[anim_name]
            if anim_data['active'] and current_time < anim_data['start_time'] + anim_data['total_duration']:
                any_active = True
            elif anim_data['active']:
                anim_data['active'] = False
        if not any_active:
            # Clear when all animations done
            self.animation_queue.clear()
            self.current_enemy_target = None

# Global animation manager instance
animation_manager = AnimationManager()
