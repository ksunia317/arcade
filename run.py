import arcade
import random


level = 1
# 0 - для текста
# 1 - для рамок
# 2 - для щаливки интерфейса
# 3 - для кнопок действий
colors = {
    1 :  [(255,152,27), (0, 50, 0), (0, 20, 0)]
}


class Run(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (0, 0, 0)
        self.selected_indx = 0
        self.selected = 0
    
    def setup(self):
        self.generate_run()
    
    def on_draw(self):
        self.clear()
        self.draw_UI()
    
    def draw_UI(self):
        arcade.draw_lrbt_rectangle_filled(0, 800, 0, 250, colors[level][2])
        arcade.draw_line(0, 250, 800, 250, colors[level][1], line_width=5)
        arcade.draw_line(0, 150, 800, 150, colors[level][1], line_width=5)
        arcade.draw_line(150, 150, 150, 0, colors[level][1], line_width=5)
        self.draw_room()
    
    def draw_room(self):
        self.background_color = self.rooms[self.indx]["background"]
        menu = self.rooms[self.indx]["actions"]
        arcade.draw_rect_outline(arcade.rect.XYWH(450, 200, 80, 80), colors[level][0])
        arcade.draw_text(menu[1],
                         450, 200,
                         colors[level][0],
                         font_size=12,
                         anchor_x="center",
                         anchor_y="center",
                         rotation=0)
        arcade.draw_rect_outline(arcade.rect.XYWH(350, 200, 80, 80), colors[level][0])
        arcade.draw_text(menu[0],
                         350, 200,
                         colors[level][0],
                         font_size=12,
                         anchor_x="center",
                         anchor_y="center",
                         rotation=0)
        arcade.draw_text(self.rooms[-1]["text"],
                         400, 800 - 30,
                         colors[level][0],
                         font_size=20,
                         anchor_x="center",
                         anchor_y="center",
                         rotation=0)
        self.draw_card()
        if self.selected == 2:
            arcade.draw_rect_filled(arcade.rect.XYWH(450, 200, 80, 80), colors[level][0])
            self.disagree()
        elif self.selected == 1:
            arcade.draw_rect_filled(arcade.rect.XYWH(350, 200, 80, 80), colors[level][0])
            self.agree()
        self.selected = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (x >= 450 - 80 // 2 and x <= 450 + 80 // 2
                and y >= 200 - 40 and y <= 200 + 40):
                self.selected = 2
            elif (x >= 350 - 40 and x <= 350 + 40
                and y >= 200 - 40 and y <= 240):
                self.selected = 1
            else:
                self.selected = 0
        else:
            self.selected = 0

    def generate_run(self):
        self.rooms = []
        data = {"card": {"border_color": (255, 255, 255),
                         "background": (100, 100, 100),
                         "text": "Пьяный Эльф",
                         "text_color": (255, 255, 0)},
                "actions": ["ДА", "Нет"],
                "background": (0, 0, 0),
                "text": "Хочешь потусить?",
                "text_color": (0, 0, 0)}
        self.rooms.append(data)
        self.indx = 0
        return
        self.indx = 0
        self.rooms = []
        for i in range(10):
            data = {"card": {},
                    "actions": [],
                    "background": (0, 0, 0),
                    "text": "ПРИВЕТ",
                    "text_color": (0, 0, 0)}

    def draw_card(self):
        card = self.rooms[-1]["card"]
        arcade.draw_lrbt_rectangle_filled(275, 525,
                                           300, 700,
                                           card["background"])
        arcade.draw_lrbt_rectangle_outline(275, 525,
                                           300, 700,
                                           card["border_color"],
                                           border_width=5)
        arcade.draw_text(card["text"],
                         (275 + 525) // 2, 700 - 20,
                         card["text_color"],
                         font_size=15,
                         anchor_x="center",
                         anchor_y="center",
                         rotation=0)

    def agree(self):
        card = self.rooms[-1]["card"]
        card["agree"]()
    
    def disagree(self):
        card = self.rooms[-1]["card"]
        card["disagree"]()


def main():
    window = arcade.Window(800, 800, "GAME", resizable=False)
    menu_view = Run()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()