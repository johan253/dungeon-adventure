class Button:
    def __init__(self, image, position, text_input, font, color_1, color_2):
        self.image = image
        self.x_position = position[0]
        self.y_position = position[1]
        self.text_input = text_input
        self.font = font
        self.color_1 = color_1
        self.color_2 = color_2
        self.text = self.font.render(self.text_input, True, self.color_1)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_position, self.y_position))
        self.text_rect = self.text.get_rect(center=(self.x_position, self.y_position))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.color_2)
        else:
            self.text = self.font.render(self.text_input, True, self.color_1)

    def check_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False
