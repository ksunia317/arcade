import random
import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle


class DustEffect:
    def __init__(self):
        self.dust_texture = arcade.make_soft_circle_texture(
            4, arcade.color.WHITE, 255, 180
        )
        self.emitters = []

    def create_dust_effect(self, x, y):

        def dust_mutator(p):
            p.change_y += -0.05
            p.change_x *= 0.95
            p.change_y *= 0.95

        emitter = Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(15),  # 15 частиц за раз
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=self.dust_texture,
                change_xy=(random.uniform(-2, 2), random.uniform(1, 3)),  # скорость
                lifetime=random.uniform(0.5, 1.2),  # время жизни
                start_alpha=200,
                end_alpha=0,
                scale=random.uniform(0.3, 0.7),
                mutation_callback=dust_mutator,
            ),
        )
        return emitter

    def add_effect(self, x, y):
        self.emitters.append(self.create_dust_effect(x, y))

    def update(self, delta_time):
        emitters_copy = self.emitters.copy()
        for emitter in emitters_copy:
            emitter.update(delta_time)
            if emitter.can_reap():
                self.emitters.remove(emitter)

    def draw(self):
        for emitter in self.emitters:
            emitter.draw()

    def clear(self):
        self.emitters.clear()