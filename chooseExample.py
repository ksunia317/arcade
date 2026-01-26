import arcade

# Настройки окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Меню в Arcade"

# Цвета
BACKGROUND_COLOR = arcade.color.DARK_BLUE
TEXT_COLOR = arcade.color.WHITE
HIGHLIGHT_COLOR = arcade.color.YELLOW

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.menu_items = ["Начать игру", "Настройки", "Выход"]
        self.selected_index = 0  # Текутельно выделенный пункт

    def setup():
        arcade.start_render()
        

    def on_draw(self):
        self.clear()
        
        # Фон
        arcade.set_background_color(BACKGROUND_COLOR)
        
        # Заголовок
        arcade.draw_text(
            "ГЛАВНОЕ МЕНЮ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            TEXT_COLOR,
            font_size=36,
            anchor_x="center",
            anchor_y="center"
        )
        
        # Пункты меню
        for i, item in enumerate(self.menu_items):
            color = HIGHLIGHT_COLOR if i == self.selected_index else TEXT_COLOR
            arcade.draw_text(
                item,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - i * 50,
                color,
                font_size=24,
                anchor_x="center",
                anchor_y="center"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif key == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        elif key == arcade.key.ENTER:
            self.select_item()

    def select_item(self):
        selected_text = self.menu_items[self.selected_index]
        if selected_text == "Начать игру":
            print("Запускаем игру!")
            # Здесь можно переключиться на игровой экран
        elif selected_text == "Настройки":
            print("Открываем настройки")
            # Здесь логика для настроек
        elif selected_text == "Выход":
            print("Выход из игры")
            arcade.close_window()

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
