import arcade
from .constants import WIDTH, HEIGHT


class Player(arcade.Sprite):
    def __init__(self, texture_path, texture_flip_path, scale=0.5):
        super().__init__(texture_path, scale)
        self.texture_flip = arcade.load_texture(texture_flip_path)
        self.texture_normal = self.texture
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 4
        self.change_x = 0
        self.change_y = 0

    def update_animation(self, direction):
        if direction == "left":
            self.texture = self.texture_normal
        elif direction == "right":
            self.texture = self.texture_flip

    def stop(self):
        self.change_x = 0
