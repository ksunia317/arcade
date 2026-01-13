import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "CardMan Game Arcade"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        arcade.draw_text("CARDMAN ARCADE", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, arcade.color.GOLD, 60,
                         anchor_x="center", font_name="Kenney Future")
        arcade.draw_text(
            "Игра-лабиринт", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220, arcade.color.LIGHT_GRAY, 24,
            anchor_x="center", font_name="Kenney Future")
        menu_options = [("Начать игру", "start"), ("Загрузить игру", "load"), ("Настройки", "settings"),
                        ("Обучение", "tutorial"), ("Выйти", "exit")]
        button_height = SCREEN_HEIGHT // 2
        for i, (text, _) in enumerate(menu_options):
            y_pos = button_height - i * 70
            color = arcade.color.WHITE if i == 0 else arcade.color.LIGHT_GRAY
            arcade.draw_text(text, SCREEN_WIDTH // 2, y_pos, color, 36,
                             anchor_x="center", font_name="Kenney Future")
            if i == 0:
                arcade.draw_line(SCREEN_WIDTH // 2 - 150, y_pos - 10, SCREEN_WIDTH // 2 + 150, y_pos - 10,
                                 arcade.color.GOLD, 3)
        arcade.draw_text("Используйте ENTER для подтверждения", SCREEN_WIDTH // 2, 50, arcade.color.LIGHT_GRAY,
                         20,  anchor_x="center", font_name="Kenney Future")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            self.window.show_view(game_view)
        elif key == arcade.key.ESCAPE:
            arcade.exit()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.DARK_BLUE_GRAY

    def on_draw(self):
        self.clear()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
