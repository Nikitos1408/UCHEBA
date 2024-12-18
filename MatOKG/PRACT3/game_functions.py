import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import pickle

SAVE_FILE = "savefile.pkl"

def check_events(ai_settings, screen, ship, bullets, stats, aliens):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            check_menu_buttons(ai_settings, screen, ship, bullets, stats, aliens, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_s:
        save_game(stats, ship, aliens, bullets, ai_settings)
    elif event.key == pygame.K_l:
        load_game(stats, ship, aliens, bullets, ai_settings, screen)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, ship, aliens, bullets):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    draw_level(screen, stats)
    pygame.display.flip()

def draw_level(screen, stats):
    font = pygame.font.Font(None, 36)

    text_surface = font.render(f"Level: {stats.level}", True, (0, 0, 0))
    save_text_surface = font.render("Сохранить - S", True, (0, 0, 0))

    text_rect = text_surface.get_rect()
    save_text_rect = save_text_surface.get_rect()

    text_rect.topleft = (10, 10)
    save_text_rect.topright = (790, 10)

    screen.blit(text_surface, text_rect)
    screen.blit(save_text_surface, save_text_rect)

def update_bullets(ai_settings, screen, stats, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        ai_settings.explosion_sound.play()
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3* alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
    
def update_aliens(ai_settings, screen, stats, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    ai_settings.fleet_direction *= -1
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

def ship_hit(ai_settings, screen, stats, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        ai_settings.ship_hit_sound.play()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        ai_settings.game_over_sound.play()
        stats.game_active = False
        stats.reset_stats()
        
def check_aliens_bottom(ai_settings, screen, stats, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, ship, aliens, bullets)
            break

def save_game(stats, ship, aliens, bullets, ai_settings):
    game_data = {
        "level": stats.level,
        "ships_left": stats.ships_left,
        "ship_center": ship.center,
        "aliens": [(alien.x, alien.rect.y) for alien in aliens.sprites()],
        "bullets": [(bullet.rect.x, bullet.y) for bullet in bullets.sprites()],
        "alien_settings": {
            "alien_speed_factor": ai_settings.alien_speed_factor,
            "fleet_drop_speed": ai_settings.fleet_drop_speed,
            "fleet_direction": ai_settings.fleet_direction
        },
        "ship_settings":{
            "ship_speed_factor": ai_settings.ship_speed_factor
        }
        
    }
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(game_data, f)

def load_game(stats, ship, aliens, bullets, ai_settings, screen):
    try:
        with open(SAVE_FILE, "rb") as f:
            game_data = pickle.load(f)
        
        stats.level = game_data["level"]
        stats.ships_left = game_data["ships_left"]
        ship.center = game_data["ship_center"]
        
        ai_settings.alien_speed_factor = game_data["alien_settings"]["alien_speed_factor"]
        ai_settings.fleet_drop_speed = game_data["alien_settings"]["fleet_drop_speed"]
        ai_settings.fleet_direction = game_data["alien_settings"]["fleet_direction"]

        ai_settings.ship_speed_factor = game_data["ship_settings"]["ship_speed_factor"]

        aliens.empty()
        for alien_x, alien_y in game_data["aliens"]:
            alien = Alien(ai_settings, screen)
            alien.x = alien_x
            alien.rect.x = alien_x
            alien.rect.y = alien_y
            aliens.add(alien)
            
        bullets.empty()
        for bullet_x, bullet_y in game_data["bullets"]:
             new_bullet = Bullet(ai_settings, screen, ship)
             new_bullet.rect.x = bullet_x
             new_bullet.y = bullet_y
             new_bullet.rect.y = bullet_y
             bullets.add(new_bullet)
        stats.game_active = True
    except FileNotFoundError:
        print("No save file found.")

def draw_menu(screen, ai_settings):
    screen.fill(ai_settings.bg_color)
    font = pygame.font.Font(None, 72)
    name_font = pygame.font.Font(None, 32)

    title_text = font.render("Инопланетное вторжение", True, (0, 0, 0))
    title_name = name_font.render("Выполнил: Угарин Никита Александрович", True, (0, 0, 0))

    title_rect = title_text.get_rect(center=(ai_settings.screen_width // 2, ai_settings.screen_height // 3))
    name_rect = title_name.get_rect(center=(ai_settings.screen_width // 2, ai_settings.screen_height // 2 + 260))
    
    button_font = pygame.font.Font(None, 48)
    
    new_game_text = button_font.render("Новая игра", True, (0, 0, 0))
    load_game_text = button_font.render("Загрузить игру", True, (0, 0, 0))
    
    new_game_rect = new_game_text.get_rect(center=(ai_settings.screen_width // 2, ai_settings.screen_height // 2))
    load_game_rect = load_game_text.get_rect(center=(ai_settings.screen_width // 2, ai_settings.screen_height // 2 + 60))
    
    pygame.draw.rect(screen, (200, 200, 200), new_game_rect.inflate(20, 10))
    pygame.draw.rect(screen, (200, 200, 200), load_game_rect.inflate(20, 10))

    screen.blit(title_text, title_rect)
    screen.blit(title_name, name_rect)
    screen.blit(new_game_text, new_game_rect)
    screen.blit(load_game_text, load_game_rect)
    
def check_menu_buttons(ai_settings, screen, ship, bullets, stats, aliens, mouse_x, mouse_y):
    button_font = pygame.font.Font(None, 48)
    new_game_text = button_font.render("New Game", True, (0, 0, 0))
    load_game_text = button_font.render("Load Game", True, (0, 0, 0))

    new_game_rect = new_game_text.get_rect(center=(ai_settings.screen_width // 2, ai_settings.screen_height // 2))
    load_game_rect = load_game_text.get_rect(center=(ai_settings.screen_width // 2, ai_settings.screen_height // 2 + 60))
    if new_game_rect.collidepoint(mouse_x, mouse_y):
        start_new_game(ai_settings, screen, ship, bullets, stats, aliens)
    elif load_game_rect.collidepoint(mouse_x, mouse_y):
         load_game(stats, ship, aliens, bullets, ai_settings, screen)

def start_new_game(ai_settings, screen, ship, bullets, stats, aliens):
    stats.reset_stats()
    ai_settings.initialize_dynamic_settings()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    stats.game_active = True