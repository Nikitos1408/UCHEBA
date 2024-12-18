import pygame
import numpy as np
import sys


def transform_segment(p1, p2):
    transformation_matrix = np.array([[1, 3],
                                      [4, 1]])

    new_p1 = transformation_matrix @ p1
    new_p2 = transformation_matrix @ p2
    return new_p1, new_p2


def main():
    pygame.init()

    # Определение размеров окна
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 3, Практическая 1")

    # Ввод координат отрезка
    x1, y1 = map(float, input("Введите координаты первой точки (x1, y1): ").split(" "))
    x2, y2 = map(float, input("Введите координаты второй точки (x2, y2): ").split(" "))

    # Применение преобразования
    p1 = np.array([x1, y1])
    p2 = np.array([x2, y2])
    new_p1, new_p2 = transform_segment(p1, p2)

    print(f"Исходные координаты: P1({x1:.2f}, {y1:.2f}), P2({x2:.2f}, {y2:.2f})")
    print(f"Новые координаты: P1({new_p1[0]:.2f}, {new_p1[1]:.2f}), P2({new_p2[0]:.2f}, {new_p2[1]:.2f})")

    # Основной цикл Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pygame.draw.line(screen, (255, 0, 0), (int(x1 + width // 2), height // 2 - int(y1)),
                         (int(x2 + width // 2), height // 2 - int(y2)), 5)

        pygame.draw.line(screen, (0, 0, 255), (int(new_p1[0] + width // 2), height // 2 - int(new_p1[1])),
                         (int(new_p2[0] + width // 2), height // 2 - int(new_p2[1])), 5)

        pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)
        pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()