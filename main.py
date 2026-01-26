import arcade
from random import randint, random, choice
from chooseExample import ChooseExample


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "CardMan Game Arcade"


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMAZON
        self.selected_option = 0
        self.menu_options = [("Начать игру", "start"), ("Загрузить игру", "load"), ("Настройки", "settings"),
                             ("Обучение", "tutorial"), ("Выйти", "exit")]

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        arcade.draw_text("CARDMAN ARCADE", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150,
                         arcade.color.GOLD, 60, anchor_x="center", font_name="Kenney Future")
        arcade.draw_text("Игра-лабиринт", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 220,
                         arcade.color.LIGHT_GRAY, 24, anchor_x="center", font_name="Kenney Future")
        button_height = SCREEN_HEIGHT // 2
        for i, (text, _) in enumerate(self.menu_options):
            y_pos = button_height - i * 70
            color = arcade.color.GOLD if i == self.selected_option else arcade.color.LIGHT_GRAY
            arcade.draw_text(text, SCREEN_WIDTH // 2, y_pos, color, 36,
                             anchor_x="center", font_name="Kenney Future")
            if i == self.selected_option:
                arcade.draw_line(SCREEN_WIDTH // 2 - 150, y_pos - 10,
                                 SCREEN_WIDTH // 2 + 150, y_pos - 10,
                                 arcade.color.GOLD, 3)
        arcade.draw_text("Используйте ↑↓ для навигации, ENTER для подтверждения",
                         SCREEN_WIDTH // 2, 50, arcade.color.LIGHT_GRAY,
                         20, anchor_x="center", font_name="Kenney Future")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
        elif key == arcade.key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
        elif key == arcade.key.ENTER:
            if self.selected_option == 0:
                game_view = GameView()
                self.window.show_view(game_view)
            elif self.selected_option == 4:
                arcade.exit()
        elif key == arcade.key.ESCAPE:
            arcade.exit()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                         0.3)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT


class Point(arcade.Sprite):
    def __init__(self, x, y, point_size=15):
        super().__init__()
        self.texture = arcade.make_soft_circle_texture(point_size, arcade.color.GOLD, 255, 255)
        self.center_x = x
        self.center_y = y
        self.point_size = point_size


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.player_list = None
        self.player = None
        self.maze = None
        self.maze_width = 0
        self.maze_height = 0
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0
        self.wall_list = None
        self.point_list = None
        self.points_collected = 0
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.point_list = arcade.SpriteList()
        self.points_collected = 0
        self.generate_maze_data()
        self.create_walls()
        self.player = Player()
        self.place_player_in_free_position()
        self.player_list.append(self.player)
        self.create_points()

    def generate_maze_data(self):
        width = 21
        height = 15
        maze_width = (width // 2) * 2 + 1
        maze_height = (height // 2) * 2 + 1
        maze = [[1 for _ in range(maze_width)] for _ in range(maze_height)]
        for y in range(1, maze_height - 1, 2):
            for x in range(1, maze_width - 1, 2):
                maze[y][x] = 0
        sets = {}
        next_set_id = 1
        for y in range(1, maze_height - 1, 2):
            for x in range(1, maze_width - 1, 2):
                if maze[y][x] == 0:
                    if (y, x) not in sets:
                        sets[(y, x)] = next_set_id
                        next_set_id += 1
            for x in range(1, maze_width - 3, 2):
                cur_cell = (y, x)
                right_cell = (y, x + 2)
                if sets[cur_cell] != sets[right_cell] and random() > 0.5:
                    maze[y][x + 1] = 0
                    old_set = sets[right_cell]
                    new_set = sets[cur_cell]
                    for cell, set_id in list(sets.items()):
                        if set_id == old_set:
                            sets[cell] = new_set
            if y < maze_height - 2:
                cells_set = {}
                for cell, set_id in sets.items():
                    if cell[0] == y:
                        if set_id not in cells_set:
                            cells_set[set_id] = []
                        cells_set[set_id].append(cell)
                for set_id, cells in cells_set.items():
                    connected_cells = [choice(cells)]
                    for cell in connected_cells:
                        y_cell, x_cell = cell
                        maze[y_cell + 1][x_cell] = 0
                        sets[(y_cell + 2, x_cell)] = set_id
                cells_to_remove = [cell for cell in sets.keys() if cell[0] == y]
                for cell in cells_to_remove:
                    del sets[cell]
        y = maze_height - 2
        for x in range(1, maze_width - 3, 2):
            cur_cell = (y, x)
            right_cell = (y, x + 2)
            if sets.get(cur_cell, -1) != sets.get(right_cell, -2):
                maze[y][x + 1] = 0
                if right_cell in sets:
                    old_set = sets[right_cell]
                    new_set = sets[cur_cell]
                    for cell, set_id in list(sets.items()):
                        if set_id == old_set:
                            sets[cell] = new_set
        for i in range(maze_height):
            maze[i][0] = 1
            maze[i][maze_width - 1] = 1
        for j in range(maze_width):
            maze[0][j] = 1
            maze[maze_height - 1][j] = 1
        entrance_side = choice(['left', 'top', 'bottom'])
        exit_side = choice(['left', 'top', 'bottom', 'right'])
        while exit_side == entrance_side:
            exit_side = choice(['left', 'top', 'bottom', 'right'])
        if entrance_side == 'left':
            entrance_y = randint(1, maze_height - 2)
            maze[entrance_y][0] = 0
            if maze[entrance_y][1] == 1:
                maze[entrance_y][1] = 0
        elif entrance_side == 'top':
            entrance_x = randint(1, maze_width - 2)
            maze[0][entrance_x] = 0
            if maze[1][entrance_x] == 1:
                maze[1][entrance_x] = 0
        elif entrance_side == 'bottom':
            entrance_x = randint(1, maze_width - 2)
            maze[maze_height - 1][entrance_x] = 0
            if maze[maze_height - 2][entrance_x] == 1:
                maze[maze_height - 2][entrance_x] = 0
        if exit_side == 'right':
            exit_y = randint(1, maze_height - 2)
            maze[exit_y][maze_width - 1] = 0
            if maze[exit_y][maze_width - 2] == 1:
                maze[exit_y][maze_width - 2] = 0
        elif exit_side == 'left':
            exit_x = randint(1, maze_width - 2)
            maze[exit_x][0] = 0
            if maze[exit_x][1] == 1:
                maze[exit_x][1] = 0
        elif exit_side == 'top':
            exit_x = randint(1, maze_width - 2)
            maze[0][exit_x] = 0
            if maze[1][exit_x] == 1:
                maze[1][exit_x] = 0
        elif exit_side == 'bottom':
            exit_x = randint(1, maze_width - 2)
            maze[maze_height - 1][exit_x] = 0
            if maze[maze_height - 2][exit_x] == 1:
                maze[maze_height - 2][exit_x] = 0
        self.maze = maze
        self.maze_width = maze_width
        self.maze_height = maze_height
        max_cell_width = (SCREEN_WIDTH - 100) // maze_width
        max_cell_height = (SCREEN_HEIGHT - 100) // maze_height
        self.cell_size = min(max_cell_width, max_cell_height, 40)
        self.offset_x = (SCREEN_WIDTH - maze_width * self.cell_size) // 2
        self.offset_y = (SCREEN_HEIGHT - maze_height * self.cell_size) // 2

    def create_walls(self):
        if not self.maze:
            return
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                if self.maze[y][x] == 1:
                    wall = arcade.SpriteSolidColor(
                        self.cell_size,
                        self.cell_size,
                        arcade.color.DARK_GREEN
                    )
                    wall.center_x = self.offset_x + x * self.cell_size + self.cell_size // 2
                    wall.center_y = self.offset_y + y * self.cell_size + self.cell_size // 2
                    self.wall_list.append(wall)

    def place_player_in_free_position(self):
        list_positions = []
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                if self.maze[y][x] == 0:
                    pos_x = self.offset_x + x * self.cell_size + self.cell_size // 2
                    pos_y = self.offset_y + y * self.cell_size + self.cell_size // 2
                    list_positions.append((pos_x, pos_y))
        if list_positions:
            pos_x, pos_y = choice(list_positions)
            self.player.center_x = pos_x
            self.player.center_y = pos_y

    def create_points(self):
        for _ in range(5):
            list_positions = []
            for y in range(self.maze_height):
                for x in range(self.maze_width):
                    if self.maze[y][x] == 0:
                        pos_x = self.offset_x + x * self.cell_size + self.cell_size // 2
                        pos_y = self.offset_y + y * self.cell_size + self.cell_size // 2
                        if (abs(pos_x - self.player.center_x) > self.cell_size * 2 or
                                abs(pos_y - self.player.center_y) > self.cell_size * 2):
                            list_positions.append((pos_x, pos_y))
            if list_positions:
                pos_x, pos_y = choice(list_positions)
                point = Point(pos_x, pos_y, self.cell_size // 2)
                self.point_list.append(point)

    def on_draw(self):
        self.clear()
        if self.wall_list:
            self.wall_list.draw()
        self.point_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update(delta_time)
        collisions = arcade.check_for_collision_with_list(self.player, self.wall_list)
        if collisions:
            for wall in collisions:
                if abs(self.player.center_x - wall.center_x) > abs(self.player.center_y - wall.center_y):
                    if self.player.center_x < wall.center_x:
                        self.player.right = wall.left
                    else:
                        self.player.left = wall.right
                else:
                    if self.player.center_y < wall.center_y:
                        self.player.top = wall.bottom
                    else:
                        self.player.bottom = wall.top
        points = arcade.check_for_collision_with_list(self.player, self.point_list)
        for point in points:
            point.remove_from_sprite_lists()
            self.points_collected += 1
            self.open_choose_window()

    def open_choose_window(self):
        choose_window = ChooseExample(800, 600, "Выбор карты")
        choose_window.setup()
        choose_window.run()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
        elif key == arcade.key.A:
            self.player.change_x = -self.player.speed
        elif key == arcade.key.D:
            self.player.change_x = self.player.speed
        elif key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()



if __name__ == "__main__":
    main()