import pygame
import sys
import random
from settings import *
from player import Player
from attack import MeleeAttack
from objects import GameObject

# Инициализация Pygame
pygame.init()

# Инициализация окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Гравитация и прыжки")
clock = pygame.time.Clock()

# Платформы
platforms = [
    pygame.Rect(200, 400, 200, 20),
    pygame.Rect(500, 300, 200, 20),
    pygame.Rect(300, 500, 200, 20),
    pygame.Rect(0, 600, 800, 20)
]

# Начальная позиция персонажа вне объектов
def get_valid_starting_position(excluded_objects):
    while True:
        x = random.randint(WALL_THICKNESS, WINDOW_WIDTH - PLAYER_SIZE - WALL_THICKNESS)
        y = random.randint(WALL_THICKNESS, WINDOW_HEIGHT - PLAYER_SIZE - WALL_THICKNESS)
        rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        if not any(rect.colliderect(obj.rect) for obj in excluded_objects):
            return [x, y]

# Создаем персонажа и атаку
objects = [
    GameObject(pygame.Rect(200, 150, OBJECT_SIZE, OBJECT_SIZE)),
    GameObject(pygame.Rect(400, 300, OBJECT_SIZE, OBJECT_SIZE)),
    GameObject(pygame.Rect(600, 450, OBJECT_SIZE, OBJECT_SIZE))
]

player = Player(get_valid_starting_position(objects), clock) # передаем clock в конструктор
melee_attack = MeleeAttack(player.pos)

# Переменная для отслеживания убитых объектов
destroyed_objects = set()

# Периодическое появление врагов
def spawn_enemy():
    if len(objects) >= 10:
        return
    while True:
      x = random.randint(WALL_THICKNESS, WINDOW_WIDTH - OBJECT_SIZE - WALL_THICKNESS)
      y = random.randint(WALL_THICKNESS, WINDOW_HEIGHT - OBJECT_SIZE - WALL_THICKNESS)
      new_enemy = pygame.Rect(x, y, OBJECT_SIZE, OBJECT_SIZE)
      if not new_enemy.colliderect(pygame.Rect(*player.pos, PLAYER_SIZE, PLAYER_SIZE)) and not any(new_enemy.colliderect(obj.rect) for obj in objects):
        objects.append(GameObject(new_enemy, True))
        break

time_since_last_spawn = 0
# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            elif event.key == pygame.K_RIGHT:
                player.moving_right = True
            elif event.key == pygame.K_UP:
                player.start_jump()
            elif event.key == pygame.K_SPACE: # Запускаем атаку по пробелу
                 melee_attack.start_attack()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                 player.moving_left = False
            elif event.key == pygame.K_RIGHT:
                 player.moving_right = False
    
    # Спавн врагов
    time_since_last_spawn += clock.get_time()
    if time_since_last_spawn > SPAWN_INTERVAL:
        spawn_enemy()
        time_since_last_spawn = 0

    # Обновление
    player.update(platforms)  # передаем платформы
    melee_attack.update(player.pos)
    for obj in objects:
      obj.update()

    # Рендеринг объектов
    screen.fill(WHITE)

    # Отрисовка платформ
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform)
    # Отрисовка стен
    #pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, WALL_THICKNESS))  # Верхняя стена
    #pygame.draw.rect(screen, BLACK, (0, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Левая стена
    #pygame.draw.rect(screen, BLACK, (0, WINDOW_HEIGHT - WALL_THICKNESS, WINDOW_WIDTH, WALL_THICKNESS))  # Нижняя стена
    #pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Правая стена

    # Отрисовка персонажа с перекрестием
    player.draw(screen)
    
    # Отрисовка зоны атаки
    melee_attack.draw(screen)

    # Отрисовка неподвижных объектов и врагов
    for obj in objects:
      if obj not in destroyed_objects:
          obj.draw(screen)
          # Проверка на попадание атаки
          if melee_attack.check_collision(obj.rect):
             destroyed_objects.add(obj)
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)