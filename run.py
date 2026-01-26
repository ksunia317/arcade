import arcade
import random


level = 1
# 0 - для текста
# 1 - для рамок
# 2 - для щаливки интерфейса
colors = {
    1 :  [(144, 238, 144), (0, 50, 0), (0, 20, 0)]
}

class Run(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = (0, 0, 0)
    
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

    
    def generate_run(self):
        self.rooms = []
        data = {"card": {},
                    "actions": ["Прямо", "Назад"],
                    "background": (0, 0, 0),
                    "text": "ПРИВЕТ",
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
            

def main():
    window = arcade.Window(800, 800, "GAME", resizable=False)
    menu_view = Run()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()