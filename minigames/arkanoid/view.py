import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel

from .constants import HEIGHT
from .game import ArkanoidGame
from .final_window import FinalView


class ArkanoidView(arcade.View):

    def __init__(self, level=1):
        super().__init__()
        self.background_color = arcade.color.BLACK
        self.game = ArkanoidGame(level)
        self.manager = UIManager()
        self.final_victory_shown = False

    def on_show_view(self):
        self.setup_ui()
        self.manager.enable()
        self.final_victory_shown = False

    def on_hide_view(self):
        self.manager.disable()

    def setup_ui(self):
        self.level_label = UILabel(
            text=f"Уровень: {self.game.level}",
            x=20,
            y=HEIGHT - 40,
            width=200,
            height=30,
            font_size=20,
            text_color=arcade.color.WHITE,
        )
        self.manager.add(self.level_label)

        self.pause_panel = UIBoxLayout(vertical=True, space_between=20)
        pause_label = UILabel(
            text="ПАУЗА",
            width=300,
            height=60,
            font_size=40,
            text_color=arcade.color.WHITE,
            align="center",
        )
        self.pause_panel.add(pause_label)
        continue_label = UILabel(
            text="Shift - продолжить",
            width=300,
            height=30,
            font_size=18,
            text_color=arcade.color.WHITE,
            align="center",
        )
        self.pause_panel.add(continue_label)
        menu_label = UILabel(
            text="ESC - в меню",
            width=300,
            height=30,
            font_size=18,
            text_color=arcade.color.WHITE,
            align="center",
        )
        self.pause_panel.add(menu_label)
        self.pause_anchor = UIAnchorLayout()
        self.pause_anchor.add(
            child=self.pause_panel, anchor_x="center", anchor_y="center"
        )
        self.pause_anchor.visible = False
        self.manager.add(self.pause_anchor)

        self.game_over_panel = UIBoxLayout(vertical=True, space_between=20)
        game_over_label = UILabel(
            text="GAME OVER",
            width=400,
            height=80,
            font_size=50,
            text_color=arcade.color.RED,
            align="center",
        )
        self.game_over_panel.add(game_over_label)
        restart_label = UILabel(
            text="Пробел - заново",
            width=300,
            height=30,
            font_size=18,
            text_color=arcade.color.WHITE,
            align="center",
        )
        self.game_over_panel.add(restart_label)
        menu_label2 = UILabel(
            text="ESC - в меню",
            width=300,
            height=30,
            font_size=18,
            text_color=arcade.color.WHITE,
            align="center",
        )
        self.game_over_panel.add(menu_label2)
        self.game_over_anchor = UIAnchorLayout()
        self.game_over_anchor.add(
            child=self.game_over_panel, anchor_x="center", anchor_y="center"
        )
        self.game_over_anchor.visible = False
        self.manager.add(self.game_over_anchor)

        if self.game.level < 5:
            self.victory_panel = UIBoxLayout(vertical=True, space_between=20)
            victory_label = UILabel(
                text="ПОБЕДА!",
                width=400,
                height=80,
                font_size=50,
                text_color=arcade.color.GREEN,
                align="center",
            )
            self.victory_panel.add(victory_label)

            next_text = "Пробел - следующий уровень"
            self.next_level_label = UILabel(
                text=next_text,
                width=300,
                height=30,
                font_size=18,
                text_color=arcade.color.WHITE,
                align="center",
            )
            self.victory_panel.add(self.next_level_label)

            menu_label3 = UILabel(
                text="ESC - в меню",
                width=300,
                height=30,
                font_size=18,
                text_color=arcade.color.WHITE,
                align="center",
            )
            self.victory_panel.add(menu_label3)
            self.victory_anchor = UIAnchorLayout()
            self.victory_anchor.add(
                child=self.victory_panel, anchor_x="center", anchor_y="center"
            )
            self.victory_anchor.visible = False
            self.manager.add(self.victory_anchor)

    def on_draw(self):
        self.clear()
        self.game.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.game.update(delta_time)
        self.update_ui_state()
        self.level_label.text = f"Уровень: {self.game.level}"

    def update_ui_state(self):
        if self.game.game_state == "paused":
            self.pause_anchor.visible = True
            if hasattr(self, "game_over_anchor"):
                self.game_over_anchor.visible = False
            if hasattr(self, "victory_anchor"):
                self.victory_anchor.visible = False

        elif self.game.game_state == "game_over":
            self.pause_anchor.visible = False
            self.game_over_anchor.visible = True
            if hasattr(self, "victory_anchor"):
                self.victory_anchor.visible = False

        elif self.game.game_state == "victory":
            if self.game.level == 5 and not self.final_victory_shown:
                self.final_victory_shown = True
                self.show_final_victory()
            elif hasattr(self, "victory_anchor"):
                self.pause_anchor.visible = False
                self.game_over_anchor.visible = False
                self.victory_anchor.visible = True

        else:
            self.pause_anchor.visible = False
            if hasattr(self, "game_over_anchor"):
                self.game_over_anchor.visible = False
            if hasattr(self, "victory_anchor"):
                self.victory_anchor.visible = False

    def show_final_victory(self):
        final_view = FinalView()
        self.window.show_view(final_view)

    def on_key_press(self, key, modifiers):
        if key not in (
            arcade.key.SPACE,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.LSHIFT,
            arcade.key.RSHIFT,
            arcade.key.ESCAPE,
        ):
            return

        self.game.handle_key_press(key)

        if self.game.game_state == "playing":
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game.game_state = "paused"
            elif key == arcade.key.ESCAPE:
                self.back_to_level_select()

        elif self.game.game_state == "paused":
            if key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                self.game.game_state = "playing"
            elif key == arcade.key.ESCAPE:
                self.back_to_level_select()

        elif self.game.game_state == "game_over":
            if key == arcade.key.SPACE:
                self.restart_game()
            elif key == arcade.key.ESCAPE:
                self.back_to_level_select()

        elif self.game.game_state == "victory":
            if key == arcade.key.SPACE:
                if self.game.level < 5:
                    self.next_level()
                else:
                    self.show_final_victory()
            elif key == arcade.key.ESCAPE:
                self.back_to_level_select()

    def on_key_release(self, key, modifiers):
        self.game.handle_key_release(key)

    def restart_game(self):
        self.game.restart_level()
        self.manager.clear()
        self.manager.disable()
        self.manager.enable()
        self.setup_ui()
        self.final_victory_shown = False

    def next_level(self):
        self.game.next_level()
        self.manager.clear()
        self.manager.disable()
        self.manager.enable()
        self.setup_ui()
        self.final_victory_shown = False

    def back_to_level_select(self):
        from .level_select import LevelSelectView

        level_select = LevelSelectView()
        self.window.show_view(level_select)
