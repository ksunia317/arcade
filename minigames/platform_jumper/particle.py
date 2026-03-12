import random

import arcade


class Particle:
    def __init__(self, x, y):
        # Начальные координаты частицы
        self.x = x
        self.y = y
        # Случайная скорость по осям
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(2, 8)
        # Время жизни частицы (1.0 - полностью жива)
        self.life = 1.0
        # Случайный оттенок оранжевого/красного
        self.color = (
            random.randint(200, 255),
            random.randint(100, 200),
            random.randint(50, 100),
        )
        # Случайный начальный размер
        self.size = random.uniform(3, 6)

    def update(self):
        # Обновление позиции
        self.x += self.vx
        self.y += self.vy
        # Гравитация
        self.vy -= 0.3
        # Уменьшение времени жизни
        self.life -= 0.03
        # Постепенное уменьшение размера
        self.size *= 0.98

    def draw(self):
        # Прозрачность зависит от оставшегося времени жизни
        alpha = int(self.life * 255)
        color_with_alpha = (*self.color, alpha)
        # Отрисовка круга с прозрачностью
        arcade.draw_circle_filled(self.x, self.y, self.size, color_with_alpha)


class ParticleSystem:
    def __init__(self):
        # Список активных частиц
        self.particles = []

    def emit(self, x, y, count=15):
        # Создание новых частиц в указанной точке
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def update(self):
        # Обновление всех частиц
        # Использование копии списка для безопасного удаления во время итерации
        for particle in self.particles[:]:
            particle.update()
            # Удаление "мертвых" частиц
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self):
        # Отрисовка всех частиц
        for particle in self.particles:
            particle.draw()

    def clear(self):
        # Полная очистка системы частиц
        self.particles.clear()
