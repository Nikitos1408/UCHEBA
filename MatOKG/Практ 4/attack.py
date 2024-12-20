import pygame
from settings import *

class MeleeAttack:
    def __init__(self, pos):
       self.pos = pos
       self.range = ATTACK_RANGE
       self.duration = ATTACK_DURATION
       self.attacking = False
       self.attack_timer = 0

    def start_attack(self):
        self.attacking = True
        self.attack_timer = self.duration
    
    def update(self, player_pos):
        self.pos = player_pos
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False

    def draw(self, screen):
        if self.attacking:
             attack_rect = pygame.Rect(self.pos[0] - self.range // 2, self.pos[1] - self.range // 2, self.range, self.range)
             pygame.draw.rect(screen, RED, attack_rect)
    
    def check_collision(self, obj_rect):
        if self.attacking:
           attack_rect = pygame.Rect(self.pos[0] - self.range // 2, self.pos[1] - self.range // 2, self.range, self.range)
           return attack_rect.colliderect(obj_rect)
        return False