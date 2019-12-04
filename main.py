import json
import pygame

# Constants to define the scale of our tiles and screen
DIVIDER_WIDTH = 1
ACTION_BAR_HEIGHT = 40
CELL_WIDTH = 20
CELL_HEIGHT = 20
CELL_COUNT_X = 32
CELL_COUNT_Y = 32

# Calculate the actual pixel dimensions of our window
WINDOW_WIDTH = CELL_WIDTH * CELL_COUNT_X + DIVIDER_WIDTH * (CELL_COUNT_X - 1)
WINDOW_HEIGHT = CELL_HEIGHT * CELL_COUNT_Y + DIVIDER_WIDTH * (CELL_COUNT_Y - 1) + ACTION_BAR_HEIGHT

# TODO: Pick good cell colors
# Color scheme constants
# noinspection PyArgumentList
ACTION_BAR_COLOR = pygame.Color(255, 255, 102)
# noinspection PyArgumentList
CELL_COLOR_EMPTY = pygame.Color(240, 240, 240)
# noinspection PyArgumentList
CELL_COLOR_WALL = pygame.Color(60, 60, 60)
# noinspection PyArgumentList
CELL_COLOR_EXPLORED = pygame.Color(0, 255, 0)
CELL_COLOR_START = CELL_COLOR_EXPLORED
CELL_COLOR_DESTINATION = CELL_COLOR_EMPTY

DEFAULT_LEVEL = "default-level.json"


class Level(object):
    def __init__(self, file_name: str = DEFAULT_LEVEL):
        with open(file_name) as level_file:
            data = json.load(level_file)
            # A 2D array of booleans to signify where the walls are in the level
            walls = data["walls"]
            self.cells = []
            for x in range(0, CELL_COUNT_X):
                column = []
                for y in range(0, CELL_COUNT_Y):
                    window_x = x * (CELL_WIDTH + DIVIDER_WIDTH)
                    window_y = y * (CELL_HEIGHT + DIVIDER_WIDTH) + ACTION_BAR_HEIGHT
                    rect = pygame.Rect(window_x, window_y, CELL_WIDTH, CELL_HEIGHT)
                    column.append(Cell(rect, x, y, walls[x][y]))
                self.cells.append(column)

        self.update_neighbors()

    def update_neighbors(self):
        for column in self.cells:
            for cell in column:
                self.define_neighbors(cell)

    def adjacency_dict(self):
        dicta = {}
        for column in self.cells:
            for cell in column:
                dicta[cell] = cell.neighbors
        return dicta

    def get_cell(self, x, y):
        return self.cells[x][y]

    def get_cell_from_window(self, window_x, window_y):
        for column in self.cells:
            for cell in column:
                if cell.rect.collidepoint(window_x, window_y):
                    return cell

    def set_wall(self, cell):
        if cell is not None:
            cell.set_wall()

    def render(self, surface: pygame.Surface):
        rects = []
        for column in self.cells:
            for cell in column:
                rect = pygame.draw.rect(surface, cell.color, cell.rect)
                rects.append(rect)
        return rects

    def define_neighbors(self, cell):
        x = cell.x
        y = cell.y

        if cell.is_wall:
            cell.neighbors = []
            return

        if x != 0:
            cell.add_neighbor(self.cells[x - 1][y])
            if y != 0:
                cell.add_neighbor(self.cells[x - 1][y - 1])
            if y != CELL_COUNT_Y - 1:
                cell.add_neighbor(self.cells[x - 1][y + 1])

        if x != CELL_COUNT_X - 1:
            cell.add_neighbor(self.cells[x + 1][y])
            if y != 0:
                cell.add_neighbor(self.cells[x + 1][y - 1])
            if y != CELL_COUNT_Y - 1:
                cell.add_neighbor(self.cells[x + 1][y + 1])

        if y != 0:
            cell.add_neighbor(self.cells[x][y - 1])

        if y != CELL_COUNT_Y - 1:
            cell.add_neighbor(self.cells[x][y + 1])


class Cell(object):
    def __init__(self, rect: pygame.Rect, x, y, is_wall: bool):
        self.x = x
        self.y = y
        self.rect = rect
        self.color = CELL_COLOR_WALL if is_wall else CELL_COLOR_EMPTY
        self.neighbors = []
        self.is_wall = is_wall

    def add_neighbor(self, neighbor: "Cell"):
        if not neighbor.is_wall:
            self.neighbors.append(neighbor)

    def set_wall(self):
        self.is_wall = True
        self.color = CELL_COLOR_WALL

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class ActionBar(object):
    def __init__(self):
        self.rect = pygame.Rect((0, 0, WINDOW_WIDTH, ACTION_BAR_HEIGHT))
        self.color = ACTION_BAR_COLOR
        # TODO: Create action buttons

    def render(self, surface: pygame.Surface):
        # TODO: render each button
        return pygame.draw.rect(surface, self.color, self.rect)


class Button(object):
    def __init__(self, text: str, rect: pygame.Rect, color: pygame.Color):
        self.text = text
        self.rect = rect
        self.color = color
        self.font = pygame.font.Font(None, 12)

    def render(self, surface):
        # TODO: Render using font.render() and surface.blit()
        pass


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize the action bar
    action_bar = ActionBar()

    # Initialize the default level
    level = Level()
    mouse_held = False

    while True:
        # Handle events in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False

        # changes cells to wall when mouse is drug over
        mouse_pos = pygame.mouse.get_pos()
        mouse_cell = level.get_cell_from_window(mouse_pos[0], mouse_pos[1])
        if mouse_held:
            level.set_wall(mouse_cell)
        level.update_neighbors()

        # Render frame to screen
        updates = level.render(window)
        updates.append(action_bar.render(window))
        pygame.display.update(updates)

        # Wait 30 milliseconds between frames
        pygame.time.wait(30)


if __name__ == "__main__":
    main()
