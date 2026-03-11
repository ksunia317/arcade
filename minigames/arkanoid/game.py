import random
import arcade

from .constants import (
    WIDTH,
    HEIGHT,
    BRICK_WIDTH,
    BRICK_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT,
    BALL_RADIUS,
    BALL_SPEED,
    PADDLE_SPEED,
    LIVES,
)
from .particles import DustEffect


class ArkanoidGame:

    def __init__(self, level=1):
        self.level = level
        self.lives = LIVES
        self.score = 0
        self.game_state = "playing"
        self.heart_texture = arcade.load_texture("assets/minigames/heart.png")
        self.bounce_sound = arcade.load_sound("sounds/bounce.mp3")
        self.background_texture = arcade.load_texture(
            "images/mini_games_background_arkanoid.png"
        )
        self.dust_effect = DustEffect()
        self.paddle_list = None
        self.ball_list = None
        self.brick_list = None
        self.paddle = None
        self.ball = None
        self.held_keys = []
        self.setup()

    def load_level(self, level_num):
        bricks_positions = []
        filename = f"minigames/arkanoid/levels/level{level_num}.txt"
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("row:"):
                parts = line.split(",")
                row = int(parts[0].split(":")[1])
                col_part = parts[1].split(":")[1]
                if "-" in col_part:
                    start, end = map(int, col_part.split("-"))
                    for col in range(start, end + 1):
                        bricks_positions.append((row, col))
                else:
                    cols = col_part.split(",")
                    for col in cols:
                        bricks_positions.append((row, int(col)))
        return bricks_positions

    def setup(self):
        self.dust_effect.clear()
        self.create_paddle()
        self.paddle.center_x = WIDTH // 2
        self.paddle.center_y = 50
        self.paddle_list = arcade.SpriteList()
        self.paddle_list.append(self.paddle)
        self.ball = arcade.SpriteCircle(BALL_RADIUS, arcade.color.YELLOW_ROSE)
        self.ball.center_x = WIDTH // 2
        self.ball.center_y = HEIGHT // 2
        self.ball.change_x = random.choice([-1, 1]) * BALL_SPEED
        self.ball.change_y = -BALL_SPEED
        self.ball_list = arcade.SpriteList()
        self.ball_list.append(self.ball)
        self.brick_list = arcade.SpriteList()
        self.generate_bricks(self.load_level(self.level))

    def create_paddle(self):
        self.paddle = arcade.Sprite("assets/minigames/platform.png")
        self.paddle.width = PADDLE_WIDTH
        self.paddle.height = PADDLE_HEIGHT
        self.paddle.center_x = WIDTH // 2
        self.paddle.center_y = 50

    def generate_bricks(self, bricks_positions):
        start_x = BRICK_WIDTH // 2 + 20
        start_y = HEIGHT - 100
        colors = [
            arcade.color.RED,
            arcade.color.ORANGE,
            arcade.color.YELLOW,
            arcade.color.GREEN,
            arcade.color.BLUE,
            arcade.color.PURPLE,
        ]
        for row, col in bricks_positions:
            brick = arcade.SpriteSolidColor(
                BRICK_WIDTH - 2, BRICK_HEIGHT - 2, colors[row % len(colors)]
            )
            brick.center_x = start_x + col * BRICK_WIDTH
            brick.center_y = start_y - row * BRICK_HEIGHT
            self.brick_list.append(brick)

    def handle_key_press(self, key):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            if key not in self.held_keys:
                self.held_keys.append(key)

    def handle_key_release(self, key):
        if key in self.held_keys:
            self.held_keys.remove(key)

    def update(self, delta_time):
        if self.game_state != "playing":
            return
        if arcade.key.LEFT in self.held_keys:
            self.paddle.center_x = max(
                self.paddle.width // 2, self.paddle.center_x - PADDLE_SPEED
            )
        elif arcade.key.RIGHT in self.held_keys:
            self.paddle.center_x = min(
                WIDTH - self.paddle.width // 2, self.paddle.center_x + PADDLE_SPEED
            )
        self.ball.center_x += self.ball.change_x
        self.ball.center_y += self.ball.change_y
        if self.ball.left <= 0 or self.ball.right >= WIDTH:
            self.ball.change_x *= -1
            self.ball.center_x = max(
                BALL_RADIUS, min(WIDTH - BALL_RADIUS, self.ball.center_x)
            )
            arcade.play_sound(self.bounce_sound)
        if self.ball.top >= HEIGHT:
            self.ball.change_y *= -1
            self.ball.center_y = min(HEIGHT - BALL_RADIUS, self.ball.center_y)
            arcade.play_sound(self.bounce_sound)
        if arcade.check_for_collision(self.ball, self.paddle):
            relative_x = (self.ball.center_x - self.paddle.center_x) / (
                self.paddle.width // 2
            )
            self.ball.change_x = relative_x * BALL_SPEED
            self.ball.change_y = abs(self.ball.change_y)
            self.ball.center_y = self.paddle.top + BALL_RADIUS
            arcade.play_sound(self.bounce_sound)
        brick_hit_list = arcade.check_for_collision_with_list(
            self.ball, self.brick_list
        )
        for brick in brick_hit_list:
            self.dust_effect.add_effect(brick.center_x, brick.center_y)
            brick.remove_from_sprite_lists()
            if abs(self.ball.center_x - brick.center_x) > abs(
                self.ball.center_y - brick.center_y
            ):
                self.ball.change_x *= -1
            else:
                self.ball.change_y *= -1
            arcade.play_sound(self.bounce_sound)
        self.dust_effect.update(delta_time)

        if self.ball.bottom <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = "game_over"
            else:
                self.respawn_ball()

        if len(self.brick_list) == 0:
            self.game_state = "victory"

    def respawn_ball(self):
        self.ball.center_x = self.paddle.center_x
        self.ball.center_y = self.paddle.top + BALL_RADIUS
        self.ball.change_x = random.choice([-1, 1]) * BALL_SPEED
        self.ball.change_y = BALL_SPEED

    def restart_level(self, level=None):
        if level is not None:
            self.level = level
        self.lives = LIVES
        self.game_state = "playing"
        self.held_keys.clear()
        self.setup()

    def next_level(self):
        if self.level < 5:
            self.level += 1
            self.restart_level()

    def draw(self):
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT),
        )
        self.brick_list.draw()
        self.paddle_list.draw()
        self.ball_list.draw()
        self.dust_effect.draw()
        heart_size = 30
        heart_spacing = 35
        start_x = WIDTH - 150
        for i in range(self.lives):
            x = start_x + i * heart_spacing
            y = HEIGHT - 30
            arcade.draw_texture_rect(
                self.heart_texture, arcade.rect.XYWH(x, y, heart_size, heart_size)
            )

    def reset_for_new_game(self):
        self.held_keys.clear()
        self.game_state = "playing"
