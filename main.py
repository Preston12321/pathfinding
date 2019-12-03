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
    # TODO: Load level file in constructor
    def __init__(self, file_name: str = DEFAULT_LEVEL):
        self.cells = []
        for x in range(0, CELL_COUNT_X - 1):
            column = []
            for y in range(0, CELL_COUNT_Y - 1):
                window_x = x * (CELL_WIDTH + DIVIDER_WIDTH)
                window_y = y * (CELL_HEIGHT + DIVIDER_WIDTH)
                rect = pygame.Rect(window_x, window_y, CELL_WIDTH, CELL_HEIGHT)
                # TODO: Get cell info from level file
                column.append(Cell(rect))
            self.cells.append(column)

    def get_cell(self, x, y):
        return self.cells[x][y]

    def render(self):
        pass


class Cell(object):
    def __init__(self, rect: pygame.Rect, is_wall: bool):
        self.rect = rect
        self.color = CELL_COLOR_WALL if is_wall else CELL_COLOR_EMPTY


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize the default level
    level = Level()

    clock = pygame.time.Clock()

    # TODO: This code was copy-pasted, probably not what we want; should change
    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    window.blit(background, (0, 0))
    overlays.draw(window)
    pygame.display.flip()


if __name__ == "__main__":
    main()

