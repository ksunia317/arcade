import arcade
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIFlatButton, UILabel, UIManager

WIDTH = 800
HEIGHT = 600

COLOR_PARCHMENT = (245, 235, 220)
COLOR_DARK_OAK = (89, 66, 41)
COLOR_OCHRE = (176, 128, 44)
COLOR_GOLD = (212, 175, 55)
COLOR_SILVER = (192, 192, 192)


class MiniGamesView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = COLOR_PARCHMENT
        self.manager = UIManager()
        self.setup()

    def on_show_view(self):
        # Активация UI
        self.manager.enable()
        self.setup_widgets()

    def on_hide_view(self):
        # Деактивация UI при скрытии
        self.manager.disable()

    def setup(self):
        # Загрузка фоновой текстуру
        self.texture = arcade.load_texture('images/menu_backgroud.png')

    def setup_widgets(self):
        # UI-элементы
        anchor_layout = UIAnchorLayout()
        box_layout = UIBoxLayout(vertical=True, space_between=10)

        title_label = UILabel(
            text='Мини-игры',
            width=300,
            height=100,
            font_size=56,
            text_color=COLOR_PARCHMENT,
            bold=True,
        )
        box_layout.add(title_label)

        # Данные для кнопок: текст и обработчик
        buttons_data = [
            ('Flappy Bird', self.flap_game_open),
            ('Platform Jumper', self.jump_game_open),
            ('Arkanoid', self.arkanoid_game_open),
            ('Таблица рекордов', self.open_records),
            ('Назад', self.back_to_menu),
        ]

        for text, func in buttons_data:
            button = UIFlatButton(width=200, height=50, text=text)
            # Стили для разных состояний кнопки
            button.style = {
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
            button.on_click = func
            box_layout.add(button)

        anchor_layout.add(child=box_layout, anchor_x='center_x', anchor_y='center_y')
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        # Отрисовка фона
        arcade.draw_texture_rect(
            self.texture, arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT),
        )
        self.manager.draw()

    def open_records(self, event=None):
        from windows.records import RecordsView
        records_view = RecordsView()
        self.window.show_view(records_view)

    def flap_game_open(self, event=None):
        from minigames.flappy_bird.view import FlappyBirdView
        flappy_view = FlappyBirdView()
        self.window.show_view(flappy_view)

    def jump_game_open(self, event=None):
        from minigames.platform_jumper.view import PlatformJumperView
        jumper_view = PlatformJumperView()
        self.window.show_view(jumper_view)

    def arkanoid_game_open(self, event=None):
        from minigames.arkanoid.level_select import LevelSelectView
        arkanoid_view = LevelSelectView()
        self.window.show_view(arkanoid_view)

    def back_to_menu(self, event=None):
        from windows.menu import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
