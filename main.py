import arcade

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "CardMan Game Arcade"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.color.AMAZON
        self.selected_option = 0
        self.menu_options = [("Начать игру", "start"), ("Загрузить игру", "load"), ("Настройки", "settings"),
                             ("Обучение", "tutorial"), ("Выйти", "exit")]

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        arcade.draw_text("CARDMAN ARCADE", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                         arcade.color.GOLD, 60, anchor_x="center", font_name="Kenney Future")
        arcade.draw_text("Игра-лабиринт", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220,
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center", font_name="Kenney Future")
        button_height = SCREEN_HEIGHT // 2
        for i, (text, _) in enumerate(self.menu_options):
            y_pos = button_height - i * 70
            color = arcade.color.GOLD if i == self.selected_option else arcade.color.LIGHT_GRAY
            arcade.draw_text(text, SCREEN_WIDTH // 2, y_pos, color, 36,
                             anchor_x="center", font_name="Kenney Future")
            if i == self.selected_option:
                arcade.draw_line(SCREEN_WIDTH // 2 - 150, y_pos - 10,
                                 SCREEN_WIDTH // 2 + 150, y_pos - 10,
                                 arcade.color.GOLD, 3)
        arcade.draw_text("Используйте ↑↓ для навигации, ENTER для подтверждения",
                         SCREEN_WIDTH // 2, 50, arcade.color.LIGHT_GRAY,
                         20, anchor_x="center", font_name="Kenney Future")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif key == arcade.key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif key == arcade.key.ENTER:
            if self.selected_option == 0:
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.selected_option == 4:
                arcade.exit()
        elif key == arcade.key.ESCAPE:
            arcade.exit()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                         0.5)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.player_list = None
        self.player = None
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = Player()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
        elif key == arcade.key.A:
            self.player.change_x = -self.player.speed
        elif key == arcade.key.D:
            self.player.change_x = self.player.speed
        elif key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
