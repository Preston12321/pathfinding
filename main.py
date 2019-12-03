import json
import pygame

# Constants to define the scale of our tiles and screen
DIVIDER_WIDTH = 1
CELL_WIDTH = 20
CELL_HEIGHT = 20
CELL_COUNT_X = 32
CELL_COUNT_Y = 32

# TODO: Add calculations for menu/actions bar at the top of the screen
# Calculate the actual pixel dimensions of our window
WINDOW_WIDTH = CELL_WIDTH * CELL_COUNT_X + DIVIDER_WIDTH * (CELL_COUNT_X - 1)
WINDOW_HEIGHT = CELL_HEIGHT * CELL_COUNT_Y + DIVIDER_WIDTH * (CELL_COUNT_Y - 1)

# TODO: Pick good cell colors
# Color scheme constants
# noinspection PyArgumentList
CELL_COLOR_EMPTY = pygame.Color(255, 255, 255)
# noinspection PyArgumentList
CELL_COLOR_WALL = pygame.Color(0, 0, 0)
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
            walls = data['walls']
            self.cells = []
            for x in range(0, CELL_COUNT_X):
                column = []
                for y in range(0, CELL_COUNT_Y):
                    window_x = x * (CELL_WIDTH + DIVIDER_WIDTH)
                    window_y = y * (CELL_HEIGHT + DIVIDER_WIDTH)
                    rect = pygame.Rect(window_x, window_y, CELL_WIDTH, CELL_HEIGHT)
                    column.append(Cell(rect, x, y, walls[x][y]))
                self.cells.append(column)

        for column in self.cells:
            for cell in column:
                self.define_neighbors(cell)

    def get_cell(self, x, y):
        return self.cells[x][y]

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

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize the default level
    level = Level()

    while True:
        pygame.time.wait(30)
        updates = level.render(window)
        pygame.display.update(updates)


if __name__ == "__main__":
    main()
