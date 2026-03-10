import arcade
from cards import CARDS

colors = {
    1: [(255, 152, 27), (0, 50, 0), (0, 20, 0)],
    2: [(100, 152, 27), (50, 0, 0), (20, 0, 0)],
}


class Run(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (0, 0, 0)
        self.selected_indx = 0
        self.selected = 0
        self.money = 50
        self.karma = 50
        self.power = 50
        self.atractive = 50
        self.attack = 5
        self.effects = []
        self.cnt = 1
        self.level = 1

    def setup(self):
        self.generate_run()

    def on_draw(self):
        self.clear()
        self.draw_UI()

    def draw_UI(self):
        arcade.draw_lrbt_rectangle_filled(0, 800, 0, 250, colors[self.level][2])
        arcade.draw_line(0, 250, 800, 250, colors[self.level][1], line_width=5)
        arcade.draw_line(0, 150, 800, 150, colors[self.level][1], line_width=5)
        arcade.draw_line(150, 150, 150, 0, colors[self.level][1], line_width=5)
        arcade.draw_text(
            str(self.cnt),
            65,
            75,
            colors[self.level][0],
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        arcade.draw_text(
            str(self.karma),
            200,
            75,
            colors[self.level][0],
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        arcade.draw_text(
            str(self.money),
            300,
            75,
            colors[self.level][0],
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        arcade.draw_text(
            str(self.atractive),
            400,
            75,
            colors[self.level][0],
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        arcade.draw_text(
            str(self.power),
            500,
            75,
            colors[self.level][0],
            font_size=40,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        self.draw_room()

    def draw_room(self):
        self.background_color = self.rooms[-1]["background"]
        menu = self.rooms[-1]["card"]["actions"]
        arcade.draw_rect_outline(
            arcade.rect.XYWH(450, 200, 80, 80), colors[self.level][0]
        )
        arcade.draw_text(
            menu[1],
            450,
            200,
            colors[self.level][0],
            font_size=12,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        arcade.draw_rect_outline(
            arcade.rect.XYWH(350, 200, 80, 80), colors[self.level][0]
        )
        arcade.draw_text(
            menu[0],
            350,
            200,
            colors[self.level][0],
            font_size=12,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        arcade.draw_text(
            self.rooms[-1]["card"]["top_text"],
            400,
            800 - 30,
            colors[self.level][0],
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        self.draw_card()
        if self.selected == 2:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(450, 200, 80, 80), colors[self.level][0]
            )
            self.disagree()
        elif self.selected == 1:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(350, 200, 80, 80), colors[self.level][0]
            )
            self.agree()
        self.selected = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (
                x >= 450 - 80 // 2
                and x <= 450 + 80 // 2
                and y >= 200 - 40
                and y <= 200 + 40
            ):
                self.selected = 2
            elif x >= 350 - 40 and x <= 350 + 40 and y >= 200 - 40 and y <= 240:
                self.selected = 1
            else:
                self.selected = 0
        else:
            self.selected = 0

    def generate_run(self):
        self.rooms = []
        data = {
            "card": CARDS["status"].copy(),
            "background": (0, 0, 0),
            "text_color": (0, 0, 0),
        }
        self.rooms.append(data)
        return

    def draw_card(self):
        card = self.rooms[-1]["card"]
        arcade.draw_lrbt_rectangle_filled(275, 525, 300, 700, card["background"])
        arcade.draw_lrbt_rectangle_outline(
            275, 525, 300, 700, card["border_color"], border_width=10
        )
        arcade.draw_text(
            card["text"],
            (275 + 525) // 2,
            700 - 20,
            card["text_color"],
            font_size=15,
            anchor_x="center",
            anchor_y="center",
            rotation=0,
        )
        self.sprite = arcade.Sprite()
        texture = arcade.load_texture(card["texture"], hit_box_algorithm=None)
        self.sprite.texture = texture
        self.sprite.center_x = 400
        self.sprite.center_y = 500
        self.sprite.scale = card["scale"]
        arcade.draw_sprite(self.sprite)

    def agree(self):
        card = self.rooms[-1]["card"]
        card["agree"](self)

    def disagree(self):
        card = self.rooms[-1]["card"]
        card["disagree"](self)

    def reset(self):
        self.karma = 50
        self.atractive = 50
        self.money = 50
        self.power = 50
        self.generate_run()
        self.cnt = 0


def main():
    window = arcade.Window(800, 800, "GAME", resizable=False)
    menu_view = Run()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
