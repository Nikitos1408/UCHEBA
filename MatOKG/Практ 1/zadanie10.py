import numpy as np
import pygame
import sys


def draw_spiral(screen, a, b, num_points=1000):
    theta = np.linspace(0, 2 * np.pi, num_points)

    r = b + 2 * a * np.cos(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    offset_x, offset_y = 300, 300

    # Отрисовка спирали
    for i in range(num_points - 1):
        pygame.draw.line(screen, (0, 0, 255),
                         (x[i] + offset_x, y[i] + offset_y),
                         (x[i + 1] + offset_x, y[i + 1] + offset_y))


def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 10, Практическая 1")

    a = 100
    b = 60

    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_spiral(screen, a, b)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()