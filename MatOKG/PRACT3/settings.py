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

class Settings():
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        self.ship_speed_factor = 1.5
        self.ship_limit = 0

        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()
    
        self.laser_sound = pygame.mixer.Sound(resource_path("sounds/laser.wav"))
        self.explosion_sound = pygame.mixer.Sound(resource_path("sounds/explosion.wav"))
        self.ship_hit_sound = pygame.mixer.Sound(resource_path("sounds/ship_hit.wav"))
        self.game_over_sound = pygame.mixer.Sound(resource_path("sounds/game_over.wav"))


    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale