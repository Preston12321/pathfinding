import pygame
import math
import action_bar as ab

# Constants to define the scale of our tiles and screen
DIVIDER_WIDTH = 1
CELL_WIDTH = 20
CELL_HEIGHT = 20
CELL_COUNT_X = 25
CELL_COUNT_Y = 25

# Hard-coded start and destination coordinates
START_NODE = (3, 4)
DESTINATION_NODE = (20, 20)

# Color scheme constants
# noinspection PyArgumentList
CELL_COLOR_EMPTY = pygame.Color(255, 255, 255)
# noinspection PyArgumentList
CELL_COLOR_WALL = pygame.Color(60, 60, 60)
# noinspection PyArgumentList
CELL_COLOR_EXPLORED = pygame.Color(31, 107, 200)
# noinspection PyArgumentList
CELL_COLOR_START = pygame.Color(107, 170, 37)
# noinspection PyArgumentList
CELL_COLOR_DESTINATION = pygame.Color(209, 38, 38)
# noinspection PyArgumentList
CELL_COLOR_CLOUD = pygame.Color(173, 216, 230)


class Level(object):
    def __init__(self):
        self.start = None
        self.destination = None
        self.cells = []
        for x in range(0, CELL_COUNT_X):
            column = []
            for y in range(0, CELL_COUNT_Y):
                # Calculate the coordinates of the top left corner of the cell
                window_x = x * (CELL_WIDTH + DIVIDER_WIDTH)
                window_y = y * (CELL_HEIGHT + DIVIDER_WIDTH) + ab.ACTION_BAR_HEIGHT

                # Create a cell with a set size and location
                rect = pygame.Rect(window_x, window_y, CELL_WIDTH, CELL_HEIGHT)
                c = Cell(rect, x, y, False)

                # If (x,y) matches START_NODE, set cell as start node
                if (x, y) == START_NODE:
                    c.set_start(True)
                    self.start = c

                # If (x,y) matches DESTINATION_NODE, set cell as destination node
                if (x, y) == DESTINATION_NODE:
                    c.set_destination(True)
                    self.destination = c

                column.append(c)
            self.cells.append(column)
        self.set_neighbors()

    def set_wall(self, wall: "Cell"):
        if wall is not None and not wall.is_start and not wall.is_destination and not wall.is_wall:
            wall.set_wall(True)
        for column in self.cells:
            for cell in column:
                if wall in cell.neighbors:
                    cell.neighbors.pop(wall)

    def set_neighbors(self):
        # Set neighbor cells of all cells
        for column in self.cells:
            for cell in column:
                self.define_neighbors(cell)

    def get_cell(self, x, y):
        return self.cells[x][y]

    def get_cell_from_window(self, window_x, window_y):
        for column in self.cells:
            for cell in column:
                if cell.rect.collidepoint(window_x, window_y):
                    return cell

    def clear_walls(self):
        for column in self.cells:
            for cell in column:
                cell.set_wall(False)
                cell.set_explored(False)
                cell.set_cloud(False)

    def clear_explored(self):
        for column in self.cells:
            for cell in column:
                cell.set_explored(False)
                cell.set_cloud(False)
                cell.set_g(math.inf)
                cell.set_f(None)

    def render(self, surface: pygame.Surface):
        rects = []

        # Render all cells onto surface
        for column in self.cells:
            for cell in column:
                rect = pygame.draw.rect(surface, cell.color, cell.rect)
                rects.append(rect)

        # Return list of areas on the window that were drawn to
        return rects

    def define_neighbors(self, cell):
        x = cell.x
        y = cell.y

        if cell.is_wall:
            cell.neighbors = {}
            return

        if x != 0:
            cell.add_neighbor(self.cells[x - 1][y], 1)
            if y != 0:
                cell.add_neighbor(self.cells[x - 1][y - 1], math.sqrt(2))
            if y != CELL_COUNT_Y - 1:
                cell.add_neighbor(self.cells[x - 1][y + 1], math.sqrt(2))

        if x != CELL_COUNT_X - 1:
            cell.add_neighbor(self.cells[x + 1][y], 1)
            if y != 0:
                cell.add_neighbor(self.cells[x + 1][y - 1], math.sqrt(2))
            if y != CELL_COUNT_Y - 1:
                cell.add_neighbor(self.cells[x + 1][y + 1], math.sqrt(2))

        if y != 0:
            cell.add_neighbor(self.cells[x][y - 1], 1)

        if y != CELL_COUNT_Y - 1:
            cell.add_neighbor(self.cells[x][y + 1], 1)


class Cell(object):
    def __init__(self, rect: pygame.Rect, x, y, is_wall: bool):
        self.x = x
        self.y = y
        self.rect = rect
        self.color = CELL_COLOR_WALL if is_wall else CELL_COLOR_EMPTY
        self.neighbors = {}
        self.is_wall = is_wall
        self.is_destination = False
        self.is_start = False
        self.is_explored = False

        self.g = math.inf
        self.f = None

    def add_neighbor(self, neighbor: "Cell", weight):
        if not neighbor.is_wall and neighbor not in self.neighbors:
            self.neighbors[neighbor] = weight

    def set_wall(self, value: bool):
        if self.is_wall == value:
            return
        if value:
            self.neighbors = {}
        self.is_wall = value
        self.color = CELL_COLOR_WALL if value else CELL_COLOR_EMPTY

    def set_destination(self, value: bool):
        if self.is_destination == value:
            return
        self.is_destination = True
        self.color = CELL_COLOR_DESTINATION if value else CELL_COLOR_EMPTY

    def set_start(self, value: bool):
        if self.is_start == value:
            return
        self.is_start = value
        self.color = CELL_COLOR_START if value else CELL_COLOR_EMPTY

    def set_explored(self, value: bool):
        if self.is_destination or self.is_start or self.is_wall:
            return
        if self.is_explored == value:
            return
        self.is_explored = value
        self.color = CELL_COLOR_EXPLORED if value else CELL_COLOR_EMPTY

    def set_cloud(self, value: bool):
        if self.is_destination or self.is_start or self.is_wall:
            return
        self.color = CELL_COLOR_CLOUD if value else CELL_COLOR_EMPTY

    def set_g(self, value):
        self.g = value

    def set_f(self, value):
        self.f = value

    def get_g(self):
        return self.g

    def get_f(self):
        return self.f

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __lt__(self, other):
        return self.f < other.f
