import arcade
from arcade.gui import *
from miniGameFlappyBird import FlappyBirdView
from miniGamePlatformJumper import PlatformJumperView
from miniGameArkanoid import ArkanoidView
from menu import MenuView

WIDTH = 800
HEIGHT = 600
TITLE = "Мини-игры"


class MiniGamesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.BEIGE
        self.manager = UIManager()

    def on_show_view(self):
        self.manager.enable()
        self.setup_widgets()

    def on_hide_view(self):
        self.manager.disable()

    def setup_widgets(self):
        anchor_layout = UIAnchorLayout()
        box_layout = UIBoxLayout(vertical=True, space_between=10)
        title_label = UILabel(text="Мини-игры", width=300, height=100, font_size=56, text_color=arcade.color.BLACK)
        box_layout.add(title_label)

        buttons_data = [
            ('Flappy Bird', self.flap_game_open),
            ('Platform Jumper', self.jump_game_open),
            ('Arkanoid', self.arkanoid_game_open)
        ]

        for text, func in buttons_data:
            button = UIFlatButton(width=200, height=50, text=text)
            button.style = {
                "normal": UIFlatButton.UIStyle(bg=arcade.color.DARK_BLUE, border=None, font_color=arcade.color.WHITE),
                "hover": UIFlatButton.UIStyle(bg=arcade.color.LIGHT_GRAY, border=None, font_color=arcade.color.BLACK),
                "press": UIFlatButton.UIStyle(bg=arcade.color.GRAY, border=None, font_color=arcade.color.WHITE)}
            button.on_click = func
            box_layout.add(button)

        anchor_layout.add(child=box_layout, anchor_x="left", anchor_y="top", align_x=50, align_y=-100)
        self.manager.add(anchor_layout)

        exit_texture = arcade.load_texture("assets/exit_button.png")
        exit_button = UITextureButton(texture=exit_texture, width=50, height=50)
        exit_button.on_click = self.back_to_menu
        exit_anchor = UIAnchorLayout()
        exit_anchor.add(child=exit_button, anchor_x="left", anchor_y="top", align_x=20, align_y=-20)
        self.manager.add(exit_anchor)

    def on_draw(self):
        self.clear()
        arcade.draw_lrbt_rectangle_filled(450, 800, 0, 800, arcade.color.LAVENDER)
        self.manager.draw()

    def flap_game_open(self, event=None):
        flappy_view = FlappyBirdView()
        self.window.show_view(flappy_view)

    def jump_game_open(self, event=None):
        jumper_view = PlatformJumperView()
        self.window.show_view(jumper_view)

    def arkanoid_game_open(self, event=None):
        arkanoid_view = ArkanoidView()
        self.window.show_view(arkanoid_view)

    def back_to_menu(self, event=None):
        menu_view = MenuView()
        self.window.show_view(menu_view)
