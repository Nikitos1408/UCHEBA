import numpy as np
import pygame
import sys


def transform_segment(segment, transformation_matrix):
    new_start = transformation_matrix @ segment[0]
    new_end = transformation_matrix @ segment[1]
    return new_start, new_end


def find_midpoint(p1, p2):
    return (p1 + p2) / 2


def main():
    pygame.init()

    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 4, Практическая 1")

    L = np.array([[-100, -150], [200, 30]])

    T = np.array([[1, 2],
                  [3, 1]])

    new_L_start, new_L_end = transform_segment(L, T)

    # Нахождение середин
    midpoint_original = find_midpoint(L[0], L[1])
    midpoint_transformed = find_midpoint(new_L_start, new_L_end)

    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Отрисовка исходного отрезка
        pygame.draw.line(screen, (255, 0, 0), (int(L[0][0] + width // 2), height // 2 - int(L[0][1])),
                         (int(L[1][0] + width // 2), height // 2 - int(L[1][1])), 5)

        # Отрисовка преобразованного отрезка
        pygame.draw.line(screen, (0, 0, 255), (int(new_L_start[0] + width // 2), height // 2 - int(new_L_start[1])),
                         (int(new_L_end[0] + width // 2), height // 2 - int(new_L_end[1])), 5)

        # Отрисовка середин (черный цвет)
        pygame.draw.circle(screen, (0, 0, 0),
                           (int(midpoint_original[0] + width // 2), height // 2 - int(midpoint_original[1])), 5)
        pygame.draw.circle(screen, (0, 0, 0),
                           (int(midpoint_transformed[0] + width // 2), height // 2 - int(midpoint_transformed[1])), 5)

        # Соединение середин отрезка
        pygame.draw.line(screen, (0, 255, 0),
                         (int(midpoint_original[0] + width // 2), height // 2 - int(midpoint_original[1])),
                         (int(midpoint_transformed[0] + width // 2), height // 2 - int(midpoint_transformed[1])), 2)

        pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)  # Ось X
        pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)  # Ось Y

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()