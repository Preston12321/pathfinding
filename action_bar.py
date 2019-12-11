import pygame

ACTION_BAR_HEIGHT = 40

# Color scheme constants
# noinspection PyArgumentList
ACTION_BAR_COLOR = pygame.Color(189, 189, 189)
# noinspection PyArgumentList
BUTTON_TEXT_COLOR = pygame.Color(255, 255, 255)
# noinspection PyArgumentList
BUTTON_COLOR_RUN = pygame.Color(160, 160, 160)
# noinspection PyArgumentList
BUTTON_COLOR_CLEAR = pygame.Color(160, 160, 160)


class ActionBar(object):
    def __init__(self, width):
        self.rect = pygame.Rect((0, 0, width, ACTION_BAR_HEIGHT))
        self.color = ACTION_BAR_COLOR
        self.buttons = []
        self.buttons.append(Button(10, 4, "Run", BUTTON_COLOR_RUN))
        self.buttons.append(Button(80, 4, "Clear", BUTTON_COLOR_CLEAR))

    def render(self, surface: pygame.Surface):
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
