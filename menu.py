import arcade
from arcade.gui import *
from miniGames import MiniGamesView

WIDTH = 800
HEIGHT = 600
TITLE = "CardMan"


class MenuView(arcade.View):
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
        title_label = UILabel(text="CardMan", width=300, height=100, font_size=56, text_color=arcade.color.BLACK)
        box_layout.add(title_label)

        buttons_data = [
            ("Играть", self.open_game),
            ("Настройки", self.open_settings),
            ("Правила", self.open_rules),
            ("Мини-игры", self.open_minigames)
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

    def on_draw(self):
        self.clear()
        arcade.draw_lrbt_rectangle_filled(400, 800, 0, 800, arcade.color.LAVENDER)
        self.manager.draw()

    def open_game(self, event=None):
        pass

    def open_settings(self, event=None):
        pass

    def open_rules(self, event=None):
        pass

    def open_minigames(self, event=None):
        mini_games_view = MiniGamesView()
        self.window.show_view(mini_games_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()