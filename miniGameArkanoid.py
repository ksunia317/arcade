import arcade
import random
from arcade.gui import *

WIDTH = 800
HEIGHT = 600
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 12
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BALL_SPEED = 5
PADDLE_SPEED = 8
LIVES = 3


class ArkanoidView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.game_state = "playing"
        self.score = 0
        self.lives = LIVES
        self.manager = UIManager()
        self.held_keys = []
        self.heart_texture = arcade.load_texture("assets/minigames/heart.png")
        self.bounce_sound = arcade.load_sound("sounds/bounce.mp3")

    def on_show_view(self):
        self.setup()
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        self.background_texture = arcade.load_texture("images/miniGames_background_Arkanoid.png")
        self.paddle = arcade.SpriteSolidColor(PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
        self.paddle.center_x = WIDTH // 2
        self.paddle.center_y = 50
        self.paddle_list = arcade.SpriteList()
        self.paddle_list.append(self.paddle)
        self.ball = arcade.SpriteCircle(BALL_RADIUS, arcade.color.WHITE)
        self.ball.center_x = WIDTH // 2
        self.ball.center_y = HEIGHT // 2
        self.ball.change_x = random.choice([-1, 1]) * BALL_SPEED
        self.ball.change_y = -BALL_SPEED
        self.ball_list = arcade.SpriteList()
        self.ball_list.append(self.ball)
        self.brick_list = arcade.SpriteList()
        self.generate_bricks()
        self.setup_widgets()

    def setup_widgets(self):
        self.score_label = UILabel(
            text=f"Счёт: {self.score}", x=20, y=HEIGHT - 40,
            width=200, height=30, font_size=20, text_color=arcade.color.WHITE
        )
        self.manager.add(self.score_label)

        self.pause_panel = UIBoxLayout(vertical=True, space_between=20)
        pause_label = UILabel(text="ПАУЗА", width=300, height=60, font_size=40, text_color=arcade.color.RED,
                              align="center")
        self.pause_panel.add(pause_label)
        continue_label = UILabel(text="Shift - продолжить", width=300, height=30, font_size=18,
                                 text_color=arcade.color.WHITE, align="center")
        self.pause_panel.add(continue_label)
        menu_label = UILabel(text="ESC - в меню", width=300, height=30, font_size=18, text_color=arcade.color.WHITE,
                             align="center")
        self.pause_panel.add(menu_label)
        self.pause_anchor = UIAnchorLayout()
        self.pause_anchor.add(child=self.pause_panel, anchor_x="center", anchor_y="center")
        self.pause_anchor.visible = False
        self.manager.add(self.pause_anchor)

        self.game_over_panel = UIBoxLayout(vertical=True, space_between=20)
        game_over_label = UILabel(text="GAME OVER", width=400, height=80, font_size=50, text_color=arcade.color.RED,
                                  align="center")
        self.game_over_panel.add(game_over_label)
        self.score_display = UILabel(text=f"Счёт: {self.score}", width=300, height=50, font_size=30,
                                     text_color=arcade.color.WHITE, align="center")
        self.game_over_panel.add(self.score_display)
        restart_label = UILabel(text="Пробел - заново", width=300, height=30, font_size=18,
                                text_color=arcade.color.WHITE, align="center")
        self.game_over_panel.add(restart_label)
        menu_label2 = UILabel(text="ESC - в меню", width=300, height=30, font_size=18, text_color=arcade.color.WHITE,
                              align="center")
        self.game_over_panel.add(menu_label2)
        self.game_over_anchor = UIAnchorLayout()
        self.game_over_anchor.add(child=self.game_over_panel, anchor_x="center", anchor_y="center")
        self.game_over_anchor.visible = False
        self.manager.add(self.game_over_anchor)

        self.victory_panel = UIBoxLayout(vertical=True, space_between=20)
        victory_label = UILabel(text="ПОБЕДА!", width=400, height=80, font_size=50, text_color=arcade.color.GREEN,
                                align="center")
        self.victory_panel.add(victory_label)
        self.victory_score_display = UILabel(text=f"Счёт: {self.score}", width=300, height=50, font_size=30,
                                             text_color=arcade.color.WHITE, align="center")
        self.victory_panel.add(self.victory_score_display)
        restart_label2 = UILabel(text="Пробел - заново", width=300, height=30, font_size=18,
                                 text_color=arcade.color.WHITE, align="center")
        self.victory_panel.add(restart_label2)
        menu_label3 = UILabel(text="ESC - в меню", width=300, height=30, font_size=18, text_color=arcade.color.WHITE,
                              align="center")
        self.victory_panel.add(menu_label3)
        self.victory_anchor = UIAnchorLayout()
        self.victory_anchor.add(child=self.victory_panel, anchor_x="center", anchor_y="center")
        self.victory_anchor.visible = False
        self.manager.add(self.victory_anchor)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background_texture, arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT))
        self.brick_list.draw()
        self.paddle_list.draw()
        self.ball_list.draw()
        heart_size = 30
        heart_spacing = 35
        start_x = WIDTH - 150
        for i in range(self.lives):
            x = start_x + i * heart_spacing
            y = HEIGHT - 30
            arcade.draw_texture_rect(self.heart_texture, arcade.rect.XYWH(x, y, heart_size, heart_size))
        self.manager.draw()

    def on_update(self, delta_time):
        if self.game_state != "playing":
            return

        if arcade.key.LEFT in self.held_keys:
            self.paddle.center_x = max(self.paddle.width // 2, self.paddle.center_x - PADDLE_SPEED)
        elif arcade.key.RIGHT in self.held_keys:
            self.paddle.center_x = min(WIDTH - self.paddle.width // 2, self.paddle.center_x + PADDLE_SPEED)

        self.ball.center_x += self.ball.change_x
        self.ball.center_y += self.ball.change_y

        if self.ball.left <= 0 or self.ball.right >= WIDTH:
            self.ball.change_x *= -1
            self.ball.center_x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, self.ball.center_x))
            arcade.play_sound(self.bounce_sound)
        if self.ball.top >= HEIGHT:
            self.ball.change_y *= -1
            self.ball.center_y = min(HEIGHT - BALL_RADIUS, self.ball.center_y)
            arcade.play_sound(self.bounce_sound)

        if arcade.check_for_collision(self.ball, self.paddle):
            relative_x = (self.ball.center_x - self.paddle.center_x) / (self.paddle.width // 2)
            self.ball.change_x = relative_x * BALL_SPEED
            self.ball.change_y = abs(self.ball.change_y)
            self.ball.center_y = self.paddle.top + BALL_RADIUS
            arcade.play_sound(self.bounce_sound)

        brick_hit_list = arcade.check_for_collision_with_list(self.ball, self.brick_list)
        for brick in brick_hit_list:
            brick.remove_from_sprite_lists()
            self.score += 10
            self.score_label.text = f"Счёт: {self.score}"
            if abs(self.ball.center_x - brick.center_x) > abs(self.ball.center_y - brick.center_y):
                self.ball.change_x *= -1
            else:
                self.ball.change_y *= -1
            arcade.play_sound(self.bounce_sound)

        if self.ball.bottom <= 0:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over()
            else:
                self.respawn_ball()

        if len(self.brick_list) == 0:
            self.victory()

    def generate_bricks(self):
        start_x = BRICK_WIDTH // 2 + 20
        start_y = HEIGHT - 100
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick = arcade.SpriteSolidColor(BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
                brick.center_x = start_x + col * BRICK_WIDTH
                brick.center_y = start_y - row * BRICK_HEIGHT
                self.brick_list.append(brick)

    def respawn_ball(self):
        self.ball.center_x = self.paddle.center_x
        self.ball.center_y = self.paddle.top + BALL_RADIUS
        self.ball.change_x = random.choice([-1, 1]) * BALL_SPEED
        self.ball.change_y = BALL_SPEED

    def victory(self):
        self.game_state = "victory"
        self.victory_score_display.text = f"Счёт: {self.score}"
        self.victory_anchor.visible = True
        self.pause_anchor.visible = False
        self.game_over_anchor.visible = False

    def game_over(self):
        self.game_state = "game_over"
        self.score_display.text = f"Счёт: {self.score}"
        self.game_over_anchor.visible = True
        self.pause_anchor.visible = False
        self.victory_anchor.visible = False

    def on_key_press(self, key, modifiers):
        if key not in (
        arcade.key.SPACE, arcade.key.LEFT, arcade.key.RIGHT, arcade.key.LSHIFT, arcade.key.RSHIFT, arcade.key.ESCAPE):
            return

        if self.game_state == "playing":
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game_state = "paused"
                self.pause_anchor.visible = True
                self.game_over_anchor.visible = False
                self.victory_anchor.visible = False
            elif key == arcade.key.ESCAPE:
                self.back_to_miniGames()
        elif self.game_state == "paused":
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game_state = "playing"
                self.pause_anchor.visible = False
            elif key == arcade.key.ESCAPE:
                self.back_to_miniGames()
        elif self.game_state == "game_over" or self.game_state == "victory":
            if key == arcade.key.SPACE:
                self.restart_game()
            elif key == arcade.key.ESCAPE:
                self.back_to_miniGames()

        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            if key not in self.held_keys:
                self.held_keys.append(key)

    def on_key_release(self, key, modifiers):
        if key in self.held_keys:
            self.held_keys.remove(key)

    def restart_game(self):
        self.game_state = "playing"
        self.score = 0
        self.lives = LIVES
        self.paddle.center_x = WIDTH // 2
        self.respawn_ball()
        self.brick_list.clear()
        self.generate_bricks()
        self.score_label.text = f"Счёт: {self.score}"
        self.score_display.text = f"Счёт: {self.score}"
        self.victory_score_display.text = f"Счёт: {self.score}"
        self.game_over_anchor.visible = False
        self.pause_anchor.visible = False
        self.victory_anchor.visible = False
        self.held_keys.clear()

    def back_to_miniGames(self):
        from miniGames import MiniGamesView
        miniGames_view = MiniGamesView()
        self.window.show_view(miniGames_view)
