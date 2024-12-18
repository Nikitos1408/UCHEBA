import numpy as np
import pygame
import sys


def transform_triangle(triangle, transformation_matrix):
    new_vertices = []
    for vertex in triangle:
        new_vertex = transformation_matrix @ vertex
        new_vertices.append(new_vertex)
    return np.array(new_vertices)


def main():
    pygame.init()

    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 9, Практическая 1")

    # Умножил для видимости
    L = np.array([[5, 1],
                  [5, 2],
                  [3, 2]]) * 100

    T = np.array([[2, 0],
                  [0, 2]])

    offset_x, offset_y = 200, 300

    L_transformed = transform_triangle(L, T) + np.array([offset_x, offset_y])
    L = L + np.array([offset_x, offset_y])

    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Отрисовка оригинального треугольника
        pygame.draw.polygon(screen, (255, 0, 0), L)

        # Отрисовка масштабированного треугольника
        pygame.draw.polygon(screen, (0, 0, 255), L_transformed)

        pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)  # Ось X
        pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)  # Ось Y

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()