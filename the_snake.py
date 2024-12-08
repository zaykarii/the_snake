from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех игровых объектов, таких как яблоки и змейки."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Базовый класс для игровых объектов."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        pass


class Apple(GameObject):
    """Класс для всех игровых объектов яблоки."""

    def __init__(self):
        """Создаёт яблоко с начальной случайной позицией."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Генерация новой случайной позиции яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для всех игровых объектов змейка."""

    def __init__(self):
        """Создаёт змейку с начальными параметрами."""
        initial_position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        super().__init__(initial_position[0], SNAKE_COLOR)
        self.positions = initial_position
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            dx, dy = self.next_direction
            if (dx * -1, dy * -1) != self.direction:  # Исключить движение
                # назад
                self.direction = self.next_direction

    def move(self):
        """Метод для управлением движения змейки"""
        # Получаем текущую позицию головы
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы на основе направления
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Проверяем столкновение с собой
        if new_head in self.positions[2:]:
            self.reset()
            return

        # Обновляем позиции змейки
        self.positions.insert(0, new_head)

        # Удаляем хвост, если длина превышает установленную,
        # и сохраняем последний сегмент
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки на экране."""
        if self.last:
            pygame.draw.rect(
                screen, BOARD_BACKGROUND_COLOR, pygame.Rect(
                    self.last, (GRID_SIZE, GRID_SIZE))
            )
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(snake):
    """Обработка нажатий клавиш управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Главные мотод программы"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
