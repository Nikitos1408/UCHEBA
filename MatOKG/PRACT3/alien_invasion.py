import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
import pickle

SAVE_FILE = "savefile.pkl"

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    
    
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, ship, aliens, bullets)
            gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets)
        else:
            gf.draw_menu(screen, ai_settings)
            pygame.display.flip()
            

run_game()