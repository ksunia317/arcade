import random

import arcade

from .constants import (
    BALL_RADIUS,
    BALL_SPEED,
    BRICK_HEIGHT,
    BRICK_WIDTH,
    HEIGHT,
    LIVES,
    PADDLE_HEIGHT,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    WIDTH,
)
from .particles import DustEffect


class ArkanoidGame:
    # Основной класс игры Арканоид
    def __init__(self, level=1):
        self.level = level
        self.lives = LIVES
        self.score = 0
        self.game_state = "playing"  # playing, game_over, victory
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
        self.held_keys = []  # список зажатых клавиш
        self.setup()

    def load_level(self, level_num):
        # Загрузка уровня из текстового файла
        bricks_positions = []
        filename = f"minigames/arkanoid/levels/level{level_num}.txt"
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('row:'):
                parts = line.split(',')
                row = int(parts[0].split(':')[1])
                col_part = parts[1].split(':')[1]

                if '-' in col_part:
                    start, end = map(int, col_part.split('-'))
                    for col in range(start, end + 1):
                        bricks_positions.append((row, col))
                else:
                    cols = col_part.split(',')
                    for col in cols:
                        bricks_positions.append((row, int(col)))

        return bricks_positions

    def setup(self):
        # Начальная настройка игры
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
        # Создание платформы
        self.paddle = arcade.Sprite('assets/minigames/platform.png')
        self.paddle.width = PADDLE_WIDTH
        self.paddle.height = PADDLE_HEIGHT
        self.paddle.center_x = WIDTH // 2
        self.paddle.center_y = 50

    def generate_bricks(self, bricks_positions):
        # Генерация кирпичей
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
                BRICK_WIDTH - 2,
                BRICK_HEIGHT - 2,
                colors[row % len(colors)],
            )
            brick.center_x = start_x + col * BRICK_WIDTH
            brick.center_y = start_y - row * BRICK_HEIGHT
            self.brick_list.append(brick)

    def handle_key_press(self, key):
        # Обработка нажатия клавиши
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            if key not in self.held_keys:
                self.held_keys.append(key)

    def handle_key_release(self, key):
        # Обработка отпускания клавиши
        if key in self.held_keys:
            self.held_keys.remove(key)

    def update(self, delta_time):
        # Обновление состояния игры
        if self.game_state != 'playing':
            return

        # Движение платформы
        if arcade.key.LEFT in self.held_keys:
            self.paddle.center_x = max(
                self.paddle.width // 2,
                self.paddle.center_x - PADDLE_SPEED,
            )
        elif arcade.key.RIGHT in self.held_keys:
            self.paddle.center_x = min(
                WIDTH - self.paddle.width // 2,
                self.paddle.center_x + PADDLE_SPEED,
            )

        # Движение мяча
        self.ball.center_x += self.ball.change_x
        self.ball.center_y += self.ball.change_y

        # Столкновение со стенами
        if self.ball.left <= 0 or self.ball.right >= WIDTH:
            self.ball.change_x *= -1
            self.ball.center_x = max(
                BALL_RADIUS,
                min(WIDTH - BALL_RADIUS, self.ball.center_x),
            )
            arcade.play_sound(self.bounce_sound)

        if self.ball.top >= HEIGHT:
            self.ball.change_y *= -1
            self.ball.center_y = min(HEIGHT - BALL_RADIUS, self.ball.center_y)
            arcade.play_sound(self.bounce_sound)

        # Столкновение с платформой
        if arcade.check_for_collision(self.ball, self.paddle):
            # Изменение направления в зависимости от места удара
            relative_x = (self.ball.center_x - self.paddle.center_x) / (
                self.paddle.width // 2
            )
            self.ball.change_x = relative_x * BALL_SPEED
            self.ball.change_y = abs(self.ball.change_y)
            self.ball.center_y = self.paddle.top + BALL_RADIUS
            arcade.play_sound(self.bounce_sound)

        # Столкновение с кирпичами
        brick_hit_list = arcade.check_for_collision_with_list(
            self.ball,
            self.brick_list,
        )
        for brick in brick_hit_list:
            self.dust_effect.add_effect(brick.center_x, brick.center_y)
            brick.remove_from_sprite_lists()

            # Определяем, с какой стороны ударились
            if abs(self.ball.center_x - brick.center_x) > abs(
                self.ball.center_y - brick.center_y
            ):
                self.ball.change_x *= -1
            else:
                self.ball.change_y *= -1

            arcade.play_sound(self.bounce_sound)

        self.dust_effect.update(delta_time)

        # Проверка выхода мяча за нижнюю границу
        if self.ball.bottom <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = 'game_over'
            else:
                self.respawn_ball()

        # Проверка победы
        if len(self.brick_list) == 0:
            self.game_state = 'victory'

    def respawn_ball(self):
        # Возрождение мяча после потери жизни
        self.ball.center_x = self.paddle.center_x
        self.ball.center_y = self.paddle.top + BALL_RADIUS
        self.ball.change_x = random.choice([-1, 1]) * BALL_SPEED
        self.ball.change_y = BALL_SPEED

    def restart_level(self, level=None):
        # Перезапуск уровня
        if level is not None:
            self.level = level
        self.lives = LIVES
        self.game_state = 'playing'
        self.held_keys.clear()
        self.setup()

    def next_level(self):
        # Переход на следующий уровень
        if self.level < 5:
            self.level += 1
            self.restart_level()

    def draw(self):
        # Отрисовка всех элементов игры
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT),
        )
        self.brick_list.draw()
        self.paddle_list.draw()
        self.ball_list.draw()
        self.dust_effect.draw()

        # Отрисовка жизней
        heart_size = 30
        heart_spacing = 35
        start_x = WIDTH - 150
        for i in range(self.lives):
            x = start_x + i * heart_spacing
            y = HEIGHT - 30
            arcade.draw_texture_rect(
                self.heart_texture,
                arcade.rect.XYWH(x, y, heart_size, heart_size),
            )

    def reset_for_new_game(self):
        # Сброс состояния для новой игры
        self.held_keys.clear()
        self.game_state = 'playing'
