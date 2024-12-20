import pygame
from settings import *

class Player:
    def __init__(self, pos, clock):
        self.pos = pos
        self.size = PLAYER_SIZE
        self.velocity = [0, 0]
        self.color = (0, 128, 255)
        self.is_jumping = False
        self.moving_left = False
        self.moving_right = False
        self.jump_timer = 0
        self.gravity_delay = 1000
        self.clock = clock # Сохраняем clock

    def update(self, platforms):
        # Горизонтальное движение
        if self.moving_left:
            self.velocity[0] = -PLAYER_SPEED
        elif self.moving_right:
            self.velocity[0] = PLAYER_SPEED
        else:
            self.velocity[0] = 0
        
        # Проверка столкновения с платформами
        player_rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        on_platform = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                on_platform = True
                if self.velocity[1] > 0:
                    self.pos[1] = platform.top - self.size
                    self.velocity[1] = 0
                    self.is_jumping = False
                    self.jump_timer = 0
                elif self.velocity[1] < 0:
                    self.pos[1] = platform.bottom
                    self.velocity[1] = 0
                    self.is_jumping = False
                    self.jump_timer = 0
        # Обновляем таймер прыжка
        if self.is_jumping:
          self.jump_timer += pygame.time.get_ticks() - (pygame.time.get_ticks() - self.clock.get_time())

        # Применяем гравитацию, если не в прыжке и не на платформе, и время прошло
        if not self.is_jumping and not on_platform:
            self.velocity[1] += GRAVITY
        elif self.is_jumping and self.jump_timer > self.gravity_delay:
            self.velocity[1] += GRAVITY
        
        # Вертикальное движение
        self.pos[0] += self.velocity[0]
        self.velocity[1] = min(self.velocity[1], 15)
        self.pos[1] += self.velocity[1]

        # Ограничение движения по краям экрана
        if self.pos[0] < WALL_THICKNESS:
            self.pos[0] = WALL_THICKNESS
        if self.pos[0] > WINDOW_WIDTH - self.size - WALL_THICKNESS:
            self.pos[0] = WINDOW_WIDTH - self.size - WALL_THICKNESS
        # Падение при выходе за нижнюю границу экрана
        if self.pos[1] > WINDOW_HEIGHT:
          self.pos[1] = WINDOW_HEIGHT - self.size
          self.velocity[1] = 0
          self.is_jumping = False
          self.jump_timer = 0
            
    def start_jump(self):
        if not self.is_jumping:
            self.velocity[1] = JUMP_FORCE
            self.is_jumping = True
            self.jump_timer = 0
    
    def draw(self, screen):
        player_rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        pygame.draw.rect(screen, self.color, player_rect)
        pygame.draw.line(screen, BLACK, (self.pos[0] + self.size // 2 - 5, self.pos[1] + self.size // 2), (self.pos[0] + self.size // 2 + 5, self.pos[1] + self.size // 2), 2)
        pygame.draw.line(screen, BLACK, (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2 - 5), (self.pos[0] + self.size // 2, self.pos[1] + self.size // 2 + 5), 2)