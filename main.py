import json
import pygame
import math
import a_star

# Constants to define the scale of our tiles and screen
DIVIDER_WIDTH = 1
ACTION_BAR_HEIGHT = 40
CELL_WIDTH = 20
CELL_HEIGHT = 20
CELL_COUNT_X = 25
CELL_COUNT_Y = 25
START_NODE = (0, 0)
DESTINATION_NODE = (5, 5)

# Calculate the actual pixel dimensions of our window
WINDOW_WIDTH = CELL_WIDTH * CELL_COUNT_X + DIVIDER_WIDTH * (CELL_COUNT_X - 1)
WINDOW_HEIGHT = CELL_HEIGHT * CELL_COUNT_Y + DIVIDER_WIDTH * (CELL_COUNT_Y - 1) + ACTION_BAR_HEIGHT

# TODO: Pick good cell colors
# Color scheme constants
# noinspection PyArgumentList
ACTION_BAR_COLOR = pygame.Color(255, 255, 255)
# noinspection PyArgumentList
BUTTON_TEXT_COLOR = pygame.Color(255, 255, 255)
# noinspection PyArgumentList
BUTTON_COLOR_RUN = pygame.Color(97, 243, 97)
# noinspection PyArgumentList
BUTTON_COLOR_CLEAR = pygame.Color(243, 97, 97)
# noinspection PyArgumentList
CELL_COLOR_EMPTY = pygame.Color(240, 240, 240)
# noinspection PyArgumentList
CELL_COLOR_WALL = pygame.Color(60, 60, 60)
# noinspection PyArgumentList
CELL_COLOR_EXPLORED = pygame.Color(0, 255, 0)
# noinspection PyArgumentList
CELL_COLOR_START = pygame.Color(0, 255, 0)
# noinspection PyArgumentList
CELL_COLOR_DESTINATION = pygame.Color(255, 0, 0)

DEFAULT_LEVEL = "blank.json"


def distance(cell_1, cell_2):
    return math.sqrt((cell_1.x - cell_2.x) ** 2 + (cell_1.y - cell_2.y) ** 2)


class Level(object):
    def __init__(self, file_name: str = DEFAULT_LEVEL):
        self.start = None
        self.destination = None

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
                    c = Cell(rect, x, y, walls[x][y])
                    if x == START_NODE[0] and y == START_NODE[1]:
                        c.set_start(True)
                        self.start = c
                    if x == DESTINATION_NODE[0] and y == DESTINATION_NODE[1]:
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
                    cell.neighbors.remove(wall)

    def set_neighbors(self):
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

    def clear_walls(self):
        for column in self.cells:
            for cell in column:
                cell.set_wall(False)

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
        self.is_destination = False
        self.is_start = False

    def add_neighbor(self, neighbor: "Cell"):
        if not neighbor.is_wall and neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def set_wall(self, value: bool):
        if self.is_wall == value:
            return
        if value:
            self.neighbors = []
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

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class ActionBar(object):
    def __init__(self):
        self.rect = pygame.Rect((0, 0, WINDOW_WIDTH, ACTION_BAR_HEIGHT))
        self.color = ACTION_BAR_COLOR
        # TODO: Create action buttons
        self.buttons = []
        self.buttons.append(Button(10, 4, "Run", BUTTON_COLOR_RUN))
        self.buttons.append(Button(80, 4, "Clear", BUTTON_COLOR_CLEAR))

    def render(self, surface: pygame.Surface):
        # TODO: render each button
        rects = [pygame.draw.rect(surface, self.color, self.rect)]
        for button in self.buttons:
            rects.append(button.render(surface))
        return rects

    def get_button_from_window(self, x, y):
        for button in self.buttons:
            if button.rect.collidepoint(x, y):
                return button
        return None


class Button(object):
    def __init__(self, x, y, text: str, color: pygame.Color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 40)
        width, height = self.font.size(text)
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, surface: pygame.Surface):
        button_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR, self.color)
        return surface.blit(button_surface, (self.x, self.y))


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize the action bar
    action_bar = ActionBar()

    # Initialize the default level
    level = Level()
    mouse_held = False
    button_clicked = None

    while True:
        # Handle events in the queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button_clicked = action_bar.get_button_from_window(event.pos[0], event.pos[1])
                    if button_clicked is None:
                        mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False
                    button_under_mouse = action_bar.get_button_from_window(event.pos[0], event.pos[1])
                    if button_clicked is not None and button_clicked is button_under_mouse:
                        # TODO: Do things based on which button was clicked
                        if button_clicked.text == "Run":
                            # TODO: Begin algorithm animation
                            a_star.a_star(level.start, level.destination)
                        if button_clicked.text == "Clear":
                            level.clear_walls()
                            level.set_neighbors()
                    button_clicked = None

        # changes cells to wall when mouse is drug over
        if mouse_held:
            mouse_pos = pygame.mouse.get_pos()
            mouse_cell = level.get_cell_from_window(mouse_pos[0], mouse_pos[1])
            level.set_wall(mouse_cell)

        # Render frame to screen
        updates = level.render(window)
        updates.extend(action_bar.render(window))
        pygame.display.update(updates)

        # Wait 30 milliseconds between frames
        pygame.time.wait(30)


if __name__ == "__main__":
    main()
