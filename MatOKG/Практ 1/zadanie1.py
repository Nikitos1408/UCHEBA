import numpy as np
import pygame

def transform_poin(x, y):
    t_matrix = np.array([[1, 3],
                       [4, 1]])

    point = np.array([x, y])

    t_point = t_matrix @ point

    return t_point

def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Задание 1, Практическая 1")

    # Ввод координат точки
    x = float(input("Введите координату x точки: "))
    y = float(input("Введите координату y точки: "))

    # Применение преобразования
    new_point = transform_poin(x, y)

    print(f"Старые координаты тогчки до преобразования: x = {x:.2f}, y = {y:.2f}")
    print(f"Новые координаты точки после преобразования: x = {new_point[0]:.2f}, y = {new_point[1]:.2f}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # фон
        screen.fill((255, 255, 255))

        # Отрисовка начальной точки (красный цвет)
        pygame.draw.circle(screen, (255, 0, 0), (int(x + width // 2), height // 2 - int(y)), 5)

        # Отрисовка новой точки (синий цвет)
        pygame.draw.circle(screen, (0, 0, 255), (int(new_point[0] + width // 2), height // 2 - int(new_point[1])), 5)

        # Отрисовка осей
        pygame.draw.line(screen, (0, 0, 0), (0, height // 2), (width, height // 2), 2)  # X-axis
        pygame.draw.line(screen, (0, 0, 0), (width // 2, 0), (width // 2, height), 2)  # Y-axis

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()