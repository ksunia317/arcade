import arcade


TEA_GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)


class ChooseExample(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=False)
        self.background_color = DARK_BLUE
        self.card_width = 180
        self.card_height = 260
        self.cards = []
        self.glows = []
        self.cards.append({"x": 200, "y": 300})
        self.cards.append({"x": 600, "y": 300})
        self.glows = [False, False]

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        for i, card in enumerate(self.cards):
            x, y = card["x"], card["y"]
            if self.glows[i]:
                arcade.draw_lrbt_rectangle_filled(
                    x - self.card_width/2 - 10,
                    x + self.card_width/2 + 10,
                    y - self.card_height/2 - 10,
                    y + self.card_height/2 + 10,
                    CYAN
                )
            arcade.draw_lrbt_rectangle_filled(
                x - self.card_width/2,
                x + self.card_width/2,
                y - self.card_height/2,
                y + self.card_height/2,
                TEA_GREEN
            )
            arcade.draw_lrbt_rectangle_outline(
                x - self.card_width/2,
                x + self.card_width/2,
                y - self.card_height/2,
                y + self.card_height/2,
                MAGENTA,
                border_width=4
            )
            arcade.draw_text(
                "К.О.Т.",
                x,
                y,
                BLACK,
                font_size=28,
                font_name="Arial",
                anchor_x="center",
                anchor_y="center"
            )

    def on_mouse_motion(self, x, y, dx, dy):
        for i, card in enumerate(self.cards):
            cx, cy = card["x"], card["y"]
            if (cx - self.card_width / 2 < x < cx + self.card_width / 2 and
                    cy - self.card_height / 2 < y < cy + self.card_height / 2):
                self.glows[i] = True
            else:
                self.glows[i] = False


def main():
    game = ChooseExample(800, 600, "Arcade Первый Контакт")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
