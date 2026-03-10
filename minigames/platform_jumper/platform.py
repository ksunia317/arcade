import random
import arcade
from .constants import PLATFORM_WIDTH, PLATFORM_HEIGHT, WIDTH, HORIZONTAL_RANGE


class Platform(arcade.Sprite):
    def __init__(self, texture_path, scale=3.0):
        super().__init__(texture_path, scale)
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT

    def set_position(self, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y

    def make_wider(self):
        self.width = PLATFORM_WIDTH * 1.5


def create_random_platform(last_platform=None, base_y=None):
    platform = Platform("assets/minigames/platform.png", scale=3.0)
    if last_platform:
        from .constants import MIN_PLATFORM_GAP, MAX_PLATFORM_GAP

        if base_y is None:
            vertical_gap = random.randint(MIN_PLATFORM_GAP, MAX_PLATFORM_GAP)
            platform.center_y = last_platform.center_y + vertical_gap
        else:
            platform.center_y = base_y
        min_x = max(PLATFORM_WIDTH // 2, last_platform.center_x - HORIZONTAL_RANGE)
        max_x = min(
            WIDTH - PLATFORM_WIDTH // 2, last_platform.center_x + HORIZONTAL_RANGE
        )
        min_x = max(min_x, PLATFORM_WIDTH)
        max_x = min(max_x, WIDTH - PLATFORM_WIDTH)
        if min_x < max_x:
            platform.center_x = random.randint(int(min_x), int(max_x))
        else:
            platform.center_x = WIDTH // 2
    else:
        platform.center_x = random.randint(PLATFORM_WIDTH, WIDTH - PLATFORM_WIDTH)
        platform.center_y = random.randint(150, 250)
    if random.random() < 0.3:
        platform.make_wider()
    return platform
