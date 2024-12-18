import pygame
import os
import sys

def resource_path(relative_path):
    try:
        # PyInstaller создает временную папку и сохраняет путь к ней в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Alien(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load(resource_path("images/alien.bmp"))
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)
        self.rect.x = self.x
        self.rect.y = self.rect.height
        
    
    def blitme(self):
         self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False