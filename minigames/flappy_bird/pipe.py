import arcade
import random
from .constants import PIPE_SPEED, PIPE_GAP, MIN_HEIGHT, MAX_HEIGHT


class Pipe(arcade.Sprite):
    def __init__(self, image, scale=1):
        super().__init__(image, scale)
        self.speed = PIPE_SPEED
        self.scored = False

    def update(self):
        self.center_x += self.speed


class PipePair:
    def __init__(self, x, window_height):
        self.bottom_pipe = Pipe("assets/minigames/pipe-red.png", scale=1.0)
        self.top_pipe = Pipe("assets/minigames/pipe-red.png", scale=1.0)
        bottom_height = random.randint(MIN_HEIGHT, MAX_HEIGHT)
        self.bottom_pipe.center_x = x
        self.bottom_pipe.center_y = bottom_height / 2
        self.bottom_pipe.height = bottom_height
        self.top_pipe.center_x = x
        self.top_pipe.center_y = (
            bottom_height + PIPE_GAP + (window_height - bottom_height - PIPE_GAP) / 2
        )
        self.top_pipe.height = window_height - bottom_height - PIPE_GAP
        self.top_pipe.angle = 180
        self.scored = False

    def update(self):
        self.bottom_pipe.update()
        self.top_pipe.update()

    def draw(self):
        self.bottom_pipe.draw(pixelated=True)
        self.top_pipe.draw(pixelated=True)

    def check(self):
        return self.bottom_pipe.right < -100
