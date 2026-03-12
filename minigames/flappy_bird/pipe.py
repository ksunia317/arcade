import random

import arcade

from .constants import MAX_HEIGHT, MIN_HEIGHT, PIPE_GAP, PIPE_SPEED


class Pipe(arcade.Sprite):
    def __init__(self, image, scale=1):
        super().__init__(image, scale)
        self.speed = PIPE_SPEED  # Скорость движения трубы
        self.scored = False  # Флаг: засчитано ли очко

    def update(self):
        self.center_x += self.speed  # Движение трубы


class PipePair:
    def __init__(self, x, window_height):
        # Создание труб
        self.bottom_pipe = Pipe('assets/minigames/pipe-red.png', scale=1.0)
        self.top_pipe = Pipe('assets/minigames/pipe-red.png', scale=1.0)

        # Случайная высота нижней трубы
        bottom_height = random.randint(MIN_HEIGHT, MAX_HEIGHT)

        # Настройка нижней трубы
        self.bottom_pipe.center_x = x
        self.bottom_pipe.center_y = bottom_height / 2
        self.bottom_pipe.height = bottom_height

        # Настройка верхней трубы
        self.top_pipe.center_x = x
        self.top_pipe.center_y = (
            bottom_height
            + PIPE_GAP
            + (window_height - bottom_height - PIPE_GAP) / 2
        )
        self.top_pipe.height = window_height - bottom_height - PIPE_GAP
        self.top_pipe.angle = 180

        self.scored = False  # Флаг для пары труб

    def update(self):
        # Обновление положения обеих труб
        self.bottom_pipe.update()
        self.top_pipe.update()

    def draw(self):
        # Отрисовка трубы
        self.bottom_pipe.draw(pixelated=True)
        self.top_pipe.draw(pixelated=True)

    def check(self):
        # Проверка, ушла ли пара труб за экран
        return self.bottom_pipe.right < -100
