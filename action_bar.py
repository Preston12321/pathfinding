import pygame

ACTION_BAR_HEIGHT = 40

# Color scheme constants
# noinspection PyArgumentList
ACTION_BAR_COLOR = pygame.Color(189, 189, 189)
# noinspection PyArgumentList
BUTTON_TEXT_COLOR = pygame.Color(255, 255, 255)
# noinspection PyArgumentList
BUTTON_COLOR_RUN = pygame.Color(107, 170, 37)
# noinspection PyArgumentList
BUTTON_COLOR_CLEAR = pygame.Color(209, 38, 38)


class ActionBar(object):
    def __init__(self, width):
        self.rect = pygame.Rect((0, 0, width, ACTION_BAR_HEIGHT))
        self.color = ACTION_BAR_COLOR

        # Create buttons
        self.buttons = []
        self.buttons.append(Button(10, 4, "Run", BUTTON_COLOR_RUN))
        self.buttons.append(Button(80, 4, "Clear", BUTTON_COLOR_CLEAR))

    def render(self, surface: pygame.Surface):
        # Render self onto surface
        rects = [pygame.draw.rect(surface, self.color, self.rect)]

        # Render buttons onto surface
        for button in self.buttons:
            rects.append(button.render(surface))

        # Return list of rectangles encoding the areas that were drawn to
        return rects

    def get_button_from_window(self, x, y):
        # Find and return the button that overlaps (x,y)
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

        # Set font to the default system font with a reasonable size
        self.font = pygame.font.Font(None, 40)

        # Set dimensions to the size needed to display the given text in the above font
        width, height = self.font.size(text)
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, surface: pygame.Surface):
        # Render text onto a new surface
        button_surface = self.font.render(self.text, True, BUTTON_TEXT_COLOR, self.color)

        # Render text surface onto given surface and return the area that was drawn to
        return surface.blit(button_surface, (self.x, self.y))
