import numpy as np
import pygame
import sys


def transform_segment(segment, transformation_matrix):
    new_start = transformation_matrix @ segment[0]
    new_end = transformation_matrix @ segment[1]
    return new_start, new_end


def main():
    pygame.init()

    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 6, Практическая 1")

    # Умножил для видимости
    L = np.array([[(-1 / 2) * 100, (3 / 2) * 100],
                  [3 * 100, (-2) * 100],
                  [(-1) * 100, (-1) * 100],
                  [3 * 100, (5 / 3) * 100]])

    # Матрица преобразования T
    T = np.array([[1, 2],
                  [1, -3]])

    # Преобразование отрезков
    new_L_start1, new_L_end1 = transform_segment(L[0:2], T)
    new_L_start2, new_L_end2 = transform_segment(L[2:4], T)

    # Сдвигаем отрезки в видимую область
    offset_x = 400
    offset_y = 300

    # Применяем смещение
    new_L_start1 += [offset_x, offset_y]
    new_L_end1 += [offset_x, offset_y]
    new_L_start2 += [offset_x, offset_y]
    new_L_end2 += [offset_x, offset_y]

    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Отрисовка исходных отрезков (красный цвет)
        pygame.draw.line(screen, (255, 0, 0), (int(L[0][0] + offset_x), height - int(L[0][1] + offset_y)),
                         (int(L[1][0] + offset_x), height - int(L[1][1] + offset_y)), 5)
        pygame.draw.line(screen, (255, 0, 0), (int(L[2][0] + offset_x), height - int(L[2][1] + offset_y)),
                         (int(L[3][0] + offset_x), height - int(L[3][1] + offset_y)), 5)

        # Отрисовка преобразованных отрезков (синий цвет)
        pygame.draw.line(screen, (0, 0, 255), (int(new_L_start1[0]), height - int(new_L_start1[1])),
                         (int(new_L_end1[0]), height - int(new_L_end1[1])), 5)
        pygame.draw.line(screen, (0, 0, 255), (int(new_L_start2[0]), height - int(new_L_start2[1])),
                         (int(new_L_end2[0]), height - int(new_L_end2[1])), 5)

        pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)  # Ось X
        pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)  # Ось Y

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()