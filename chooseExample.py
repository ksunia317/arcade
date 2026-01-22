import arcade  # Подключаем игровые суперсилы



class ChooseExample(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=False)
        self.background_color = arcade.color.TEA_GREEN
        

    def setup(self):
        """ Инициализируем игру здесь. Вызывается один раз при запуске игры """
        # Пока тут пусто. Скоро наполним жизнью!
        pass

    def on_draw(self):
        self.clear()


def main():
    game = ChooseExample(800, 600, "Arcade Первый Контакт")
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()