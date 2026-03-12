import arcade

from .constants import WIDTH, HEIGHT, GRAVITY, FLAP_STRENGTH


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # Загрузка звука взмаха крыльев
        self.flap_sound = arcade.load_sound('sounds/flap.mp3')
        # Текстуры для анимации полета (крылья вниз, середина, вверх)
        self.textures = [
            arcade.load_texture('assets/minigames/yellowbird-downflap.png'),
            arcade.load_texture('assets/minigames/yellowbird-midflap.png'),
            arcade.load_texture('assets/minigames/yellowbird-upflap.png'),
        ]
        self.texture = self.textures[0]  # Начальная текстура
        self.scale = 1.0
        # Стартовая позиция - слева в центре
        self.center_x = WIDTH // 4
        self.center_y = HEIGHT // 2
        self.velocity_y = 0  # Вертикальная скорость
        self.acceleration_y = 0  # Вертикальное ускорение
        self.animation_timer = 0  # Таймер для смены кадров анимации
        self.texture_index = 0  # Индекс текущей текстуры
        self.alive = True  # Жива ли птица
        self.animating = True  # Нужно ли анимировать

    def update(self):
        if not self.alive:
            # Если птица мертва - ускоренное падение
            self.acceleration_y = -GRAVITY * 2
            self.animating = False
        else:
            # Обычное падение под действием гравитации
            self.acceleration_y = -GRAVITY
            self.animating = True

        self.velocity_y += self.acceleration_y
        self.center_y += self.velocity_y

        if self.animating:
            # Смена кадров анимации
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.texture_index = (self.texture_index + 1) % len(self.textures)
                self.texture = self.textures[self.texture_index]
                self.animation_timer = 0

        # Ограничение по верхней границе
        if self.top > HEIGHT:
            self.top = HEIGHT
            self.velocity_y = 0

        # Ограничение по нижней границе
        if self.bottom < 0:
            self.bottom = 0
            self.velocity_y = 0

    def flap(self):
        # Взмах крыльями, если птица жива
        if self.alive:
            arcade.play_sound(self.flap_sound)
            self.velocity_y = FLAP_STRENGTH
