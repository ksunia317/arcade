import json

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

WIDTH = 800
HEIGHT = 600

COLOR_PARCHMENT = (245, 235, 220)
COLOR_DARK_OAK = (89, 66, 41)
COLOR_OCHRE = (176, 128, 44)
COLOR_GOLD = (212, 175, 55)
COLOR_SILVER = (192, 192, 192)
COLOR_BLACK = (0, 0, 0)
POSITION_NUMBER = 5


class RecordsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = COLOR_PARCHMENT
        self.setup()
        self.manager = UIManager()
        self.records_file = 'data/records.json'
        self.records_data = {}

    def on_show_view(self):
        self.manager.enable()
        self.load_records()
        self.setup_widgets()

    def on_hide_view(self):
        self.manager.disable()

    def setup(self):
        # Загрузка фоновую текстуру
        self.texture = arcade.load_texture('images/menu_backgroud.png')

    def load_records(self):
        # Загрузка рекордов из JSON файла
        with open(self.records_file, 'r', encoding='utf-8') as f:
            self.records_data = json.load(f)

    def setup_widgets(self):
        # Основной UI
        anchor_layout = UIAnchorLayout()
        main_vertical = UIBoxLayout(vertical=True, space_between=30)

        title_label = UILabel(
            text='Таблица рекордов',
            width=400,
            height=50,
            font_size=40,
            text_color=COLOR_PARCHMENT,
            bold=True,
            align='center',
        )
        main_vertical.add(title_label)

        # Горизонтальный контейнер для игр
        horizontal_layout = UIBoxLayout(vertical=False, space_between=40)
        games_order = ['Flappy Bird', 'Platform Jumper']

        for game_name in games_order:
            # Вертикальный контейнер для конкретной игры
            game_vertical = UIBoxLayout(vertical=True, space_between=10, align='center')

            game_title = UILabel(
                text=game_name,
                width=150,
                height=30,
                font_size=18,
                text_color=COLOR_GOLD,
                bold=True,
                align='center',
            )
            game_vertical.add(game_title)

            # Отображение рекордов игры
            game_records = self.records_data.get(game_name, [])
            for record in game_records:
                record_text = f"#{record['place']} - {record['score']}"
                record_label = UILabel(
                    text=record_text,
                    width=120,
                    height=25,
                    font_size=14,
                    text_color=COLOR_PARCHMENT,
                    align='center',
                )
                game_vertical.add(record_label)

            # Заполнение пустых мест прочерками
            for _ in range(len(game_records), POSITION_NUMBER):
                empty_label = UILabel(
                    text='—',
                    width=120,
                    height=25,
                    font_size=14,
                    text_color=COLOR_SILVER,
                    align='center',
                )
                game_vertical.add(empty_label)

            horizontal_layout.add(game_vertical)

        main_vertical.add(horizontal_layout)

        # Кнопка возврата
        back_button = UIFlatButton(width=180, height=40, text='Назад')
        back_button.style = {
            'normal': UIFlatButton.UIStyle(
                bg=COLOR_DARK_OAK, border=None, font_color=COLOR_GOLD,
            ),
            'hover': UIFlatButton.UIStyle(
                bg=COLOR_GOLD, border=None, font_color=COLOR_DARK_OAK,
            ),
            'press': UIFlatButton.UIStyle(
                bg=COLOR_OCHRE, border=None, font_color=COLOR_SILVER,
            ),
        }
        back_button.on_click = self.back_to_minigames
        main_vertical.add(back_button)

        anchor_layout.add(child=main_vertical, anchor_x='center_x', anchor_y='center_y')
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        # Отрисовка фона
        arcade.draw_texture_rect(
            self.texture, arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT),
        )
        self.manager.draw()

    def back_to_minigames(self, event=None):
        # Возврат к выбору мини-игр
        from windows.mini_games import MiniGamesView
        menu_view = MiniGamesView()
        self.window.show_view(menu_view)
