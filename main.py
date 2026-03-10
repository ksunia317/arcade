import arcade
from windows.menu import MenuView

WIDTH = 800
HEIGHT = 600
TITLE = "CardMan"


def main():
    window = arcade.Window(WIDTH, HEIGHT, TITLE, resizable=False)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
