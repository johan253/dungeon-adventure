import pygame


class TextField:
    """
    Constructor for the class TextField
    """
    def __init__(self, x, y, width, height, text='', color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.txt_surface = pygame.font.Font('Assets/Dungeon Depths.ttf', 24).render(text, True, color)
        self.active = False

    def handle_event(self, event):
        """
        This class handles the event for the text when entering user's name.
        :param event: Action take for the text field.
        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = pygame.font.Font('Assets/Dungeon Depths.ttf', 24).render(self.text, True, self.color)

    def draw(self, screen):
        """
        Draw the rectangle to insert the text on the screen.
        :param screen: Screen that the rectangle will be drawn on.
        :return:
        """
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        """
        Getter for the text.
        :return: The text.
        """
        return self.text
