import arcade
from .constants import WIDTH, HEIGHT, GRAVITY, FLAP_STRENGTH


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.flap_sound = arcade.load_sound("sounds/flap.mp3")
        self.textures = [
            arcade.load_texture("assets/minigames/yellowbird-downflap.png"),
            arcade.load_texture("assets/minigames/yellowbird-midflap.png"),
            arcade.load_texture("assets/minigames/yellowbird-upflap.png"),
        ]
        self.texture = self.textures[0]
        self.scale = 1.0
        self.center_x = WIDTH // 4
        self.center_y = HEIGHT // 2
        self.velocity_y = 0
        self.acceleration_y = 0
        self.animation_timer = 0
        self.texture_index = 0
        self.alive = True
        self.animating = True

    def update(self):
        if not self.alive:
            self.acceleration_y = -GRAVITY * 2
            self.animating = False
        else:
            self.acceleration_y = -GRAVITY
            self.animating = True
        self.velocity_y += self.acceleration_y
        self.center_y += self.velocity_y
        if self.animating:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.texture_index = (self.texture_index + 1) % len(self.textures)
                self.texture = self.textures[self.texture_index]
                self.animation_timer = 0
        if self.top > HEIGHT:
            self.top = HEIGHT
            self.velocity_y = 0
        if self.bottom < 0:
            self.bottom = 0
            self.velocity_y = 0

    def flap(self):
        if self.alive:
            arcade.play_sound(self.flap_sound)
            self.velocity_y = FLAP_STRENGTH
