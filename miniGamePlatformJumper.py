import arcade
import random
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel
from arcade.camera import Camera2D

WIDTH = 800
HEIGHT = 600
GRAVITY = 1.0
JUMP_STRENGTH = 18
PLAYER_SPEED = 5
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
CAMERA_SPEED = 2
MIN_PLATFORM_GAP = 80
MAX_PLATFORM_GAP = 150
HORIZONTAL_RANGE = 200
SKY_TEXTURE_HEIGHT = 1024


class PlatformJumperView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.SKY_BLUE
        self.game_state = "playing"
        self.score = 0
        self.death_timer = 0
        self.camera = Camera2D(position=(WIDTH // 2, HEIGHT // 2), zoom=1.0)
        self.manager = UIManager()
        self.held_keys = []
        self.physics_engine = None
        self.player_texture = "assets/minigames/jumper.png"
        self.player_texture_flip = "assets/minigames/jumper_flip.png"
        self.platform_texture = "assets/minigames/platform.png"

    def on_show_view(self):
        self.setup()
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        self.texture = arcade.load_texture("images/miniGames_background_PlatformJumper.png")
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        self.player.center_x = WIDTH // 2
        self.player.center_y = HEIGHT // 4
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)
        self.platform_list = arcade.SpriteList()
        self.init_platforms()
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platform_list, gravity_constant=GRAVITY,
            ladders=None, walls=self.platform_list)
        self.setup_widgets()

    def init_platforms(self):
        platform = arcade.Sprite(self.platform_texture, scale=3.0)
        platform.width = PLATFORM_WIDTH * 1.5
        platform.height = PLATFORM_HEIGHT
        platform.center_x = WIDTH // 2
        platform.center_y = 100
        self.platform_list.append(platform)
        current_y = 100
        for i in range(15):
            self.add_platform(current_y)
            current_y += random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)

    def add_platform(self, base_y=None):
        platform = arcade.Sprite(self.platform_texture, scale=3.0)
        platform.width = PLATFORM_WIDTH
        platform.height = PLATFORM_HEIGHT
        if self.platform_list:
            last_platform = self.platform_list[-1]
            if base_y is None:
                vertical_gap = random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
                platform.center_y = last_platform.center_y + vertical_gap
            else:
                platform.center_y = base_y
            min_x = max(PLATFORM_WIDTH // 2, last_platform.center_x - HORIZONTAL_RANGE)
            max_x = min(WIDTH - PLATFORM_WIDTH // 2, last_platform.center_x + HORIZONTAL_RANGE)
            min_x = max(min_x, PLATFORM_WIDTH)
            max_x = min(max_x, WIDTH - PLATFORM_WIDTH)
            if min_x < max_x:
                platform.center_x = random.randint(int(min_x), int(max_x))
            else:
                platform.center_x = WIDTH // 2
        else:
            platform.center_x = random.randint(PLATFORM_WIDTH, WIDTH - PLATFORM_WIDTH)
            platform.center_y = random.randint(150, 250)
        if random.random() < 0.3:
            platform.width = PLATFORM_WIDTH * 1.5
        self.platform_list.append(platform)

    def setup_widgets(self):
        self.score_label = UILabel(
            text=f"Высота: {int(self.player.center_y)}", x=20, y=HEIGHT - 40,
            width=200, height=30, font_size=20, text_color=arcade.color.BLACK)
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
        self.score_display = UILabel(text=f"Высота: {int(self.player.center_y)}", width=300, height=50, font_size=30,
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
        camera_y = self.camera.position[1]
        camera_bottom = camera_y - HEIGHT // 2
        sky_start_y = (camera_bottom // SKY_TEXTURE_HEIGHT) * SKY_TEXTURE_HEIGHT
        with self.camera.activate():
            for y_offset in range(0, HEIGHT + SKY_TEXTURE_HEIGHT, SKY_TEXTURE_HEIGHT):
                sky_y = sky_start_y + y_offset + SKY_TEXTURE_HEIGHT // 2
                arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(WIDTH // 2, sky_y, WIDTH, SKY_TEXTURE_HEIGHT))
            self.platform_list.draw()
            self.player_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        if self.game_state == "paused":
            return
        if self.game_state == "game_over":
            self.death_timer += delta_time
            return
        if self.physics_engine:
            self.physics_engine.update()
        if arcade.key.LEFT in self.held_keys:
            self.player.change_x = -PLAYER_SPEED
            self.player.texture = arcade.load_texture(self.player_texture)
        elif arcade.key.RIGHT in self.held_keys:
            self.player.change_x = PLAYER_SPEED
            self.player.texture = arcade.load_texture(self.player_texture_flip)
        else:
            self.player.change_x = 0
        camera_bottom = self.camera.position[1] - HEIGHT // 2
        for platform in self.platform_list[:]:
            if platform.top < camera_bottom - 100:
                self.platform_list.remove(platform)
        camera_top = self.camera.position[1] + HEIGHT // 2
        highest_platform = max([p.center_y for p in self.platform_list], default=0)
        if highest_platform < camera_top + 300:
            self.add_platform(highest_platform + random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP))
        if self.physics_engine:
            self.physics_engine.walls = self.platform_list
        target_y = self.player.center_y
        current_y = self.camera.position[1]
        new_y = current_y + (target_y - current_y) * CAMERA_SPEED * delta_time
        self.camera.position = (WIDTH // 2, new_y)
        self.score = max(self.score, int(self.player.center_y))
        self.score_label.text = f"Высота: {self.score - 149}"
        if self.player.top < camera_bottom - 50:
            self.game_over()

    def on_key_press(self, key, modifiers):
        if key not in (arcade.key.SPACE,
                       arcade.key.UP, arcade.key.LEFT, arcade.key.RIGHT, arcade.key.LSHIFT, arcade.key.RSHIFT,
                       arcade.key.ESCAPE):
            return
        if self.game_state == "playing":
            if key == arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player.change_y = JUMP_STRENGTH
            elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game_state = "paused"
                self.pause_anchor.visible = True
                self.game_over_anchor.visible = False
            elif key == arcade.key.ESCAPE:
                self.back_to_miniGames()
        elif self.game_state == "paused":
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game_state = "playing"
                self.pause_anchor.visible = False
            elif key == arcade.key.ESCAPE:
                self.back_to_miniGames()
        elif self.game_state == "game_over":
            if key == arcade.key.SPACE:
                self.restart_game()
            elif key == arcade.key.ESCAPE:
                self.back_to_miniGames()

        if key not in self.held_keys:
            self.held_keys.append(key)

    def game_over(self):
        self.game_state = "game_over"
        self.score_display.text = f"Высота: {self.score - 149}"
        self.game_over_anchor.visible = True
        self.pause_anchor.visible = False

    def on_key_release(self, key, modifiers):
        if key not in (arcade.key.LEFT, arcade.key.RIGHT):
            return
        if key in self.held_keys:
            self.held_keys.remove(key)
            if not (arcade.key.LEFT in self.held_keys or arcade.key.RIGHT in self.held_keys):
                self.player.change_x = 0
        else:
            if key in self.held_keys:
                self.held_keys.remove(key)

    def restart_game(self):
        self.game_state = "playing"
        self.score = 0
        self.death_timer = 0
        self.player_list.clear()
        self.player = arcade.Sprite(self.player_texture, scale=0.5)
        self.player.center_x = WIDTH // 2
        self.player.center_y = HEIGHT // 4
        self.player_list.append(self.player)
        self.platform_list.clear()
        self.init_platforms()
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.platform_list, gravity_constant=GRAVITY,
            ladders=None, walls=self.platform_list)
        self.camera.position = (WIDTH // 2, HEIGHT // 2)
        self.score_label.text = f"Высота: {self.score - 149}"
        self.score_display.text = f"Высота: {self.score - 149}"
        self.game_over_anchor.visible = False
        self.pause_anchor.visible = False
        self.held_keys.clear()

    def back_to_miniGames(self):
        from miniGames import MiniGamesView
        miniGames_view = MiniGamesView()
        self.window.show_view(miniGames_view)
