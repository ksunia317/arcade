import arcade
import random
from arcade.gui import *
from miniGames import MiniGamesView

PIPE_SPEED = -3
PIPE_GAP = 200
MIN_HEIGHT = 100
MAX_HEIGHT = 500
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10


class FlappyBirdView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.SKY_BLUE
        self.game_state = "playing"
        self.score = 0
        self.death_timer = 0
        self.pipes = []
        self.pipe_timer = 0
        self.pipe_list = arcade.SpriteList()
        self.manager = UIManager()
        self.jump_sound = arcade.load_sound("sounds/jump.mp3")

    def on_show_view(self):
        self.setup()
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        self.texture = arcade.load_texture("images/miniGames_background_FlappyBird.png")
        self.bird = Bird()
        self.bird_list = arcade.SpriteList()
        self.bird_list.append(self.bird)
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
                                 text_color=arcade.color.BLACK, align="center")
        self.pause_panel.add(continue_label)
        menu_label = UILabel(text="ESC - в меню", width=300, height=30, font_size=18, text_color=arcade.color.BLACK,
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
                                     text_color=arcade.color.BLACK, align="center")
        self.game_over_panel.add(self.score_display)
        restart_label = UILabel(text="Пробел - заново", width=300, height=30, font_size=18,
                                text_color=arcade.color.BLACK, align="center")
        self.game_over_panel.add(restart_label)
        menu_label2 = UILabel(text="ESC - в меню", width=300, height=30, font_size=18, text_color=arcade.color.BLACK,
                              align="center")
        self.game_over_panel.add(menu_label2)
        self.game_over_anchor = UIAnchorLayout()
        self.game_over_anchor.add(child=self.game_over_panel, anchor_x="center", anchor_y="center")
        self.game_over_anchor.visible = False
        self.manager.add(self.game_over_anchor)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT))
        self.pipe_list.draw()
        self.bird_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        if self.game_state == "paused":
            return

        self.bird.update()
        if self.game_state == "game_over":
            self.death_timer += delta_time
            return

        self.pipe_timer += delta_time
        if self.pipe_timer > 2.0:
            pipe_pair = PipePair(WIDTH + 100, HEIGHT)
            self.pipes.append(pipe_pair)
            self.pipe_list.append(pipe_pair.bottom_pipe)
            self.pipe_list.append(pipe_pair.top_pipe)
            self.pipe_timer = 0

        for pipe_pair in self.pipes[:]:
            pipe_pair.update()
            if pipe_pair.check():
                self.pipes.remove(pipe_pair)
                self.pipe_list.remove(pipe_pair.bottom_pipe)
                self.pipe_list.remove(pipe_pair.top_pipe)
            if not pipe_pair.scored and pipe_pair.bottom_pipe.right < self.bird.left:
                pipe_pair.scored = True
                self.score += 1
                self.score_label.text = f"Счёт: {self.score}"

        if arcade.check_for_collision_with_list(self.bird, self.pipe_list):
            self.bird.alive = False
            self.game_state = "game_over"
            self.score_display.text = f"Счёт: {self.score}"
            self.game_over_anchor.visible = True
            self.pause_anchor.visible = False

    def on_key_press(self, key, modifiers):
        if key not in (arcade.key.SPACE, arcade.key.LSHIFT, arcade.key.RSHIFT, arcade.key.ESCAPE):
            return

        if self.game_state == "playing":
            if key == arcade.key.SPACE:
                self.bird.flap()
            elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game_state = "paused"
                self.pause_anchor.visible = True
                self.game_over_anchor.visible = False
            elif key == arcade.key.ESCAPE:
                self.back_to_menu()
        elif self.game_state == "paused":
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game_state = "playing"
                self.pause_anchor.visible = False
            elif key == arcade.key.ESCAPE:
                self.back_to_menu()
        elif self.game_state == "game_over":
            if key == arcade.key.SPACE:
                self.restart_game()
            elif key == arcade.key.ESCAPE:
                self.back_to_menu()

    def restart_game(self):
        self.game_state = "playing"
        self.score = 0
        self.death_timer = 0
        self.bird_list.clear()
        self.bird = Bird()
        self.bird_list.append(self.bird)
        self.pipes.clear()
        self.pipe_list.clear()
        self.pipe_timer = 0
        self.score_label.text = f"Счёт: {self.score}"
        self.score_display.text = f"Счёт: {self.score}"
        self.game_over_anchor.visible = False
        self.pause_anchor.visible = False

    def back_to_menu(self):
        miniGames_view = MiniGamesView()
        self.window.show_view(miniGames_view)


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures = [
            arcade.load_texture("assets/yellowbird-downflap.png"),
            arcade.load_texture("assets/yellowbird-midflap.png"),
            arcade.load_texture("assets/yellowbird-upflap.png")
        ]
        self.texture = self.textures[0]
        self.scale = 1.0
        self.center_x = WIDTH // 4
        self.center_y = HEIGHT // 2
        self.velocity_y = 0
        self.animation_timer = 0
        self.texture_index = 0
        self.alive = True
        self.animating = True

    def update(self):
        if not self.alive:
            self.velocity_y -= GRAVITY * 2
            self.animating = False
        else:
            self.velocity_y += GRAVITY
            self.animating = True

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
            self.velocity_y = FLAP_STRENGTH
            arcade.play_sound(arcade.get_window().views[-1].jump_sound)


class Pipe(arcade.Sprite):
    def __init__(self, image, scale=1):
        super().__init__(image, scale)
        self.speed = PIPE_SPEED
        self.scored = False

    def update(self):
        self.center_x += self.speed


class PipePair:
    def __init__(self, x, window_height):
        self.bottom_pipe = Pipe("assets/pipe-red.png", scale=1.0)
        self.top_pipe = Pipe("assets/pipe-red.png", scale=1.0)
        bottom_height = random.randint(MIN_HEIGHT, MAX_HEIGHT)
        self.bottom_pipe.center_x = x
        self.bottom_pipe.center_y = bottom_height / 2
        self.bottom_pipe.height = bottom_height
        self.top_pipe.center_x = x
        self.top_pipe.center_y = bottom_height + PIPE_GAP + (window_height - bottom_height - PIPE_GAP) / 2
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