import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIFlatButton

from .constants import (
    WIDTH,
    HEIGHT,
    COLOR_PARCHMENT,
    COLOR_DARK_OAK,
    COLOR_OCHRE,
    COLOR_GOLD,
    COLOR_SILVER,
)


class FinalView(arcade.View):
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
        self.texture = arcade.load_texture("images/menu_backgroud.png")

    def setup_widgets(self):
        anchor_layout = UIAnchorLayout()
        main_box = UIBoxLayout(vertical=True, space_between=30)

        title_label = UILabel(
            text="ПОЗДРАВЛЯЕМ!",
            width=500,
            height=80,
            font_size=60,
            text_color=COLOR_GOLD,
            bold=True,
            align="center",
        )
        main_box.add(title_label)

        subtitle_label = UILabel(
            text="Вы прошли все 5 уровней!",
            width=400,
            height=40,
            font_size=24,
            text_color=COLOR_PARCHMENT,
            align="center",
        )
        main_box.add(subtitle_label)

        stars_label = UILabel(
            text="★★★★★",
            width=200,
            height=50,
            font_size=40,
            text_color=COLOR_GOLD,
            align="center",
        )
        main_box.add(stars_label)

        menu_button = UIFlatButton(width=250, height=60, text="Главное меню")
        menu_button.style = {
            "normal": UIFlatButton.UIStyle(
                bg=COLOR_DARK_OAK, border=None, font_color=COLOR_GOLD
            ),
            "hover": UIFlatButton.UIStyle(
                bg=COLOR_GOLD, border=None, font_color=COLOR_DARK_OAK
            ),
            "press": UIFlatButton.UIStyle(
                bg=COLOR_OCHRE, border=None, font_color=COLOR_SILVER
            ),
        }
        menu_button.on_click = self.back_to_main_menu
        main_box.add(menu_button)

        anchor_layout.add(child=main_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.texture, arcade.rect.XYWH(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT)
        )
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.back_to_main_menu()

    def back_to_main_menu(self, event=None):
        from windows.menu import MenuView

        menu_view = MenuView()
        self.window.show_view(menu_view)
