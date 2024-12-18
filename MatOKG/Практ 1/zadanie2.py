import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Задание 2, Практическая 1")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Шрифт для текста
font = pygame.font.Font(None, 36)

def main():
    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Заполнение фона
        screen.fill(BLACK)

        pygame.draw.circle(screen, RED, (200, 200), 100)
        pygame.draw.line(screen, BLUE, (100, 150), (700, 300), 5)
        pygame.draw.line(screen, GREEN, (100, 200), (700, 200), 5)
        text_surface = font.render('Угарин Никита Александрович', True, WHITE)
        screen.blit(text_surface, (320, 50))

        pygame.display.flip()

    # Завершение Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()