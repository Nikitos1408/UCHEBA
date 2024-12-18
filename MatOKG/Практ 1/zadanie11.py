import numpy as np
import pygame
import sys


def rotate_matrix(angle):
    return np.array([[np.cos(angle), -np.sin(angle)],
                     [np.sin(angle), np.cos(angle)]])


def scale_matrix(scale_factor):
    return np.array([[scale_factor, 0],
                     [0, scale_factor]])


def transform_square(square, scale_factor, angle):
    # Масштабирование
    scale = scale_matrix(scale_factor)
    scaled_square = square @ scale
    # Поворот
    rotation = rotate_matrix(angle)
    transformed_square = scaled_square @ rotation

    return transformed_square


def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 11, Практическая 1")

    # Умножил для видимости
    square = np.array([[2, -2],
                       [-2, -2],
                       [-2, 2],
                       [2, 2]]) * 100

    scale_factor = 0.9
    angle = np.pi / 32
    offset_x, offset_y = width // 2, height // 2

    # Основной цикл Pygame
    running = True
    iterations = 20
    squares_history = []
    for i in range(iterations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        square = transform_square(square, scale_factor, angle)
        square_transformed = square + np.array([offset_x, offset_y])
        pygame.draw.polygon(screen, (0, 0, 255), square_transformed, width=2)

        squares_history.append(square_transformed)

        for sq in squares_history:
            pygame.draw.polygon(screen, (0, 0, 255), sq, width=2)

        pygame.display.flip()
        pygame.time.delay(500)

    pygame.quit()


if __name__ == "__main__":
    main()