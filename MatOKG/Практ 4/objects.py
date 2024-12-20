import pygame
from settings import *
import random
class GameObject:
    def __init__(self, rect, is_enemy = False):
        self.rect = rect
        self.color = (150, 150, 150)  # серый
        self.is_enemy = is_enemy
        if self.is_enemy:
           self.color = GREEN
           self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]  # Случайная начальная скорость врага

    def update(self):
      if self.is_enemy:
         self.rect.x += self.velocity[0]
         self.rect.y += self.velocity[1]
      
         # Ограничение движения по краям экрана для врагов
         if self.rect.left < WALL_THICKNESS:
            self.velocity[0] = abs(self.velocity[0])
         if self.rect.right > WINDOW_WIDTH - WALL_THICKNESS:
            self.velocity[0] = -abs(self.velocity[0])
         if self.rect.top < WALL_THICKNESS:
            self.velocity[1] = abs(self.velocity[1])
         if self.rect.bottom > WINDOW_HEIGHT - WALL_THICKNESS:
            self.velocity[1] = -abs(self.velocity[1])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)