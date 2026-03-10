import random
import arcade


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(2, 8)
        self.life = 1.0
        self.color = (
            random.randint(200, 255),
            random.randint(100, 200),
            random.randint(50, 100),
        )
        self.size = random.uniform(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 0.3
        self.life -= 0.03
        self.size *= 0.98

    def draw(self):
        alpha = int(self.life * 255)
        color_with_alpha = (*self.color, alpha)
        arcade.draw_circle_filled(self.x, self.y, self.size, color_with_alpha)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=15):
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()

    def clear(self):
        self.particles.clear()
