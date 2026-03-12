import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

from .constants import (
    COLOR_DARK_OAK,
    COLOR_GOLD,
    COLOR_OCHRE,
    COLOR_PARCHMENT,
    COLOR_SILVER,
    HEIGHT,
    WIDTH,
)


class LevelSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = COLOR_PARCHMENT
        self.setup()
        self.manager = UIManager()

    def on_show_view(self):
        self.manager.enable()
        self.setup_widgets()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        # Загрузка текстуры фона
        self.texture = arcade.load_texture('images/menu_backgroud.png')

    def setup_widgets(self):
        anchor_layout = UIAnchorLayout()
        main_box = UIBoxLayout(vertical=True, space_between=20)

        # Заголовок
        title_label = UILabel(
            text='Выберите уровень',
            width=400,
            height=50,
            font_size=40,
            text_color=COLOR_PARCHMENT,
            bold=True,
            align='center',
        )
        main_box.add(title_label)

        # Контейнер для кнопок уровней
        levels_box = UIBoxLayout(vertical=True, space_between=10)

        for i in range(1, 6):
            level_button = UIFlatButton(
                width=200,
                height=50,
                text=f'Уровень {i}',
            )
            level_button.style = {
                'normal': UIFlatButton.UIStyle(
                    bg=COLOR_DARK_OAK,
                    border=None,
                    font_color=COLOR_GOLD,
                ),
                'hover': UIFlatButton.UIStyle(
                    bg=COLOR_GOLD,
                    border=None,
                    font_color=COLOR_DARK_OAK,
                ),
                'press': UIFlatButton.UIStyle(
                    bg=COLOR_OCHRE,
                    border=None,
                    font_color=COLOR_SILVER,
                ),
            }
            # Запоминание номера уровня
            level_button.on_click = lambda event, level=i: self.start_level(level)
            levels_box.add(level_button)

        main_box.add(levels_box)

        # Кнопка возврата
        back_button = UIFlatButton(
            width=200,
            height=50,
            text='Назад',
        )
        back_button.style = {
            'normal': UIFlatButton.UIStyle(
                bg=COLOR_DARK_OAK,
                border=None,
                font_color=COLOR_GOLD,
            ),
            'hover': UIFlatButton.UIStyle(
                bg=COLOR_GOLD,
                border=None,
                font_color=COLOR_DARK_OAK,
            ),
            'press': UIFlatButton.UIStyle(
                bg=COLOR_OCHRE,
                border=None,
                font_color=COLOR_SILVER,
            ),
        }
        back_button.on_click = self.back_to_minigames
        main_box.add(back_button)

        # Центрирование основного макета
        anchor_layout.add(
            child=main_box,
            anchor_x='center_x',
            anchor_y='center_y',
        )
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        # Отрисовка фонового изображения
        arcade.draw_texture_rect(
            self.texture,
            arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT),
        )
        self.manager.draw()

    def start_level(self, level):
        from .view import ArkanoidView

        game_view = ArkanoidView(level)
        self.window.show_view(game_view)

    def back_to_minigames(self, event=None):
        from windows.mini_games import MiniGamesView

        menu_view = MiniGamesView()
        self.window.show_view(menu_view)
