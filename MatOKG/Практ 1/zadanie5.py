import numpy as np
import pygame
import sys


def transform_segment(segment, transformation_matrix):
    # Применение матричного преобразования к концам отрезка
    new_start = transformation_matrix @ segment[0]
    new_end = transformation_matrix @ segment[1]
    return new_start, new_end


def calculate_slope(p1, p2):
    # Рассчитываем наклон отрезка
    if p2[0] - p1[0] == 0:  # Проверка деления на 0
        return float('inf')
    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def main():
    pygame.init()

    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 5, Практическая 1")

    # Исходные параллельные отрезки
    L = np.array([[50, 100], [250, 200],
                  [50, 200], [250, 300]])

    # Матрица преобразования T
    T = np.array([[1, 2],
                  [3, 1]])

    # Преобразование отрезков
    new_L_start1, new_L_end1 = transform_segment(L[0:2], T)
    new_L_start2, new_L_end2 = transform_segment(L[2:4], T)

    # Рассчитываем наклоны
    slope_original1 = calculate_slope(L[0], L[1])
    slope_original2 = calculate_slope(L[2], L[3])
    slope_transformed1 = calculate_slope(new_L_start1, new_L_end1)
    slope_transformed2 = calculate_slope(new_L_start2, new_L_end2)

    print(f"Исходные наклоны: отрезок 1: {slope_original1:.2f}, отрезок 2: {slope_original2:.2f}")
    print(f"Преобразованные наклоны: отрезок 1: {slope_transformed1:.2f}, отрезок 2: {slope_transformed2:.2f}")

    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Отрисовка исходных отрезков
        pygame.draw.line(screen, (255, 0, 0), (L[0][0], height - L[0][1]),
                         (L[1][0], height - L[1][1]), 5)
        pygame.draw.line(screen, (255, 0, 0), (L[2][0], height - L[2][1]),
                         (L[3][0], height - L[3][1]), 5)

        # Отрисовка преобразованных отрезков
        pygame.draw.line(screen, (0, 0, 255), (new_L_start1[0], height - new_L_start1[1]),
                         (new_L_end1[0], height - new_L_end1[1]), 5)
        pygame.draw.line(screen, (0, 0, 255), (new_L_start2[0], height - new_L_start2[1]),
                         (new_L_end2[0], height - new_L_end2[1]), 5)

        pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)  # Ось X
        pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)  # Ось Y

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()