import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton, UITextureButton

WIDTH = 800
HEIGHT = 600

COLOR_PARCHMENT = (245, 235, 220)
COLOR_DARK_OAK = (89, 66, 41)
COLOR_RED_WINE = (109, 26, 44)
COLOR_GOLD = (212, 175, 55)
COLOR_SILVER = (192, 192, 192)


class MiniGamesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = COLOR_PARCHMENT
        self.manager = UIManager()

    def on_show_view(self):
        self.manager.enable()
        self.setup_widgets()

    def on_hide_view(self):
        self.manager.disable()

    def setup_widgets(self):
        anchor_layout = UIAnchorLayout()
        box_layout = UIBoxLayout(vertical=True, space_between=10)
        title_label = UILabel(text="Мини-игры", width=300, height=100, font_size=56, text_color=COLOR_RED_WINE)
        box_layout.add(title_label)
        buttons_data = [
            ('Flappy Bird', self.flap_game_open),
            ('Platform Jumper', self.jump_game_open),
            ('Arkanoid', self.arkanoid_game_open)]
        for text, func in buttons_data:
            button = UIFlatButton(width=200, height=50, text=text)
            button.style = {
                "normal": UIFlatButton.UIStyle(bg=COLOR_DARK_OAK, border=None, font_color=COLOR_GOLD),
                "hover": UIFlatButton.UIStyle(bg=COLOR_GOLD, border=None, font_color=COLOR_DARK_OAK),
                "press": UIFlatButton.UIStyle(bg=COLOR_RED_WINE, border=None, font_color=COLOR_SILVER)}
            button.on_click = func
            box_layout.add(button)
        anchor_layout.add(child=box_layout, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor_layout)
        exit_texture = arcade.load_texture("assets/buttons/exit_button.png")
        exit_button = UITextureButton(texture=exit_texture, width=50, height=50)
        exit_button.on_click = self.back_to_menu
        exit_anchor = UIAnchorLayout()
        exit_anchor.add(child=exit_button, anchor_x="left", anchor_y="top", align_x=20, align_y=-20)
        self.manager.add(exit_anchor)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def flap_game_open(self, event=None):
        from miniGameFlappyBird import FlappyBirdView
        flappy_view = FlappyBirdView()
        self.window.show_view(flappy_view)

    def jump_game_open(self, event=None):
        from miniGamePlatformJumper import PlatformJumperView
        jumper_view = PlatformJumperView()
        self.window.show_view(jumper_view)

    def arkanoid_game_open(self, event=None):
        from miniGameArkanoid import ArkanoidView
        arkanoid_view = ArkanoidView()
        self.window.show_view(arkanoid_view)

    def back_to_menu(self, event=None):
        from menu import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
