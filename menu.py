import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

WIDTH = 800
HEIGHT = 600
TITLE = "CardMan"

COLOR_PARCHMENT = (245, 235, 220)
COLOR_DARK_OAK = (89, 66, 41)
COLOR_OCHRE = (184, 130, 36)
COLOR_GOLD = (212, 175, 55)
COLOR_SILVER = (192, 192, 192)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = COLOR_PARCHMENT
        self.manager = UIManager()
        self.setup()

    def setup(self):
        self.texture = arcade.load_texture("images/menu_backgroud.png")
        print(self.texture)

    def on_show_view(self):
        self.manager.enable()
        self.setup_widgets()

    def on_hide_view(self):
        self.manager.disable()

    def setup_widgets(self):
        anchor_layout = UIAnchorLayout()
        box_layout = UIBoxLayout(vertical=True, space_between=10)
        title_label = UILabel(text="CardMan", width=300, height=100, font_size=56, text_color=COLOR_PARCHMENT,
                              bold=True)
        box_layout.add(title_label)
        buttons_data = [
            ("Играть", self.open_game),
            ("Мини-игры", self.open_minigames)
        ]
        for text, func in buttons_data:
            button = UIFlatButton(width=200, height=50, text=text)
            button.style = {
                "normal": UIFlatButton.UIStyle(bg=COLOR_DARK_OAK, border=None, font_color=COLOR_GOLD),
                "hover": UIFlatButton.UIStyle(bg=COLOR_GOLD, border=None, font_color=COLOR_DARK_OAK),
                "press": UIFlatButton.UIStyle(bg=COLOR_OCHRE, border=None, font_color=COLOR_SILVER)}
            button.on_click = func
            box_layout.add(button)
        anchor_layout.add(child=box_layout, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT))
        self.manager.draw()

    def open_game(self, event=None):
        from run import Run
        self.window.set_size(800, 800)
        run_view = Run()
        run_view.setup()
        self.window.show_view(run_view)

    def open_minigames(self, event=None):
        from minigames.miniGames import MiniGamesView
        mini_games_view = MiniGamesView()
        self.window.show_view(mini_games_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE, resizable=True)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
