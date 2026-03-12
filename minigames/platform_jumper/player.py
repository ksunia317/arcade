import arcade

from .constants import WIDTH, HEIGHT


class Player(arcade.Sprite):
    def __init__(self, texture_path, texture_flip_path, scale=0.5):
        # Родительский конструктор с основной текстурой
        super().__init__(texture_path, scale)
        # Загрузка отзеркаленной текстуры
        self.texture_flip = arcade.load_texture(texture_flip_path)
        # Сохранение оригинальной текстуры
        self.texture_normal = self.texture
        # Начальная позиция платформы
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 4
        # Скорость по горизонтали и вертикали
        self.change_x = 0
        self.change_y = 0

    def update_animation(self, direction):
        # Выбор нужной текстуры в зависимости от направления
        if direction == "left":
            self.texture = self.texture_normal
        elif direction == "right":
            self.texture = self.texture_flip

    def stop(self):
        self.change_x = 0
