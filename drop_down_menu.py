import pygame


class UIDropDownMenu:
    def __init__(self, x, y, width, height, font, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.options = options
        self.selected_index = 0
        self.is_open = False

    def draw(self, screen):
        # Draw the dropdown menu
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

        # Draw the selected option
        text = self.font.render(self.options[self.selected_index], True, (0, 0, 0))
        screen.blit(text, (self.x + 5, self.y))

        # Draw the arrow to indicate that the menu can be opened
        pygame.draw.polygon(screen, (0, 0, 0),
                            [(self.x + self.width - 15, self.y + 5), (self.x + self.width - 5, self.y + 5),
                             (self.x + self.width - 10, self.y + 10)])

        # If the menu is open, draw the options
        if self.is_open:
            for i in range(len(self.options)):
                # Highlight the selected option
                # if i == self.selected_index:
                pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y + self.height + i * 20, self.width, 20))

                # Draw the option text
                text = self.font.render(self.options[i], True, (0, 0, 0))
                screen.blit(text, (self.x + 5, self.y + self.height + i * 20))

    def handle_events(self, event):
        # If the user clicks the dropdown menu, open it
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and event.pos[1] >= self.y and event.pos[
                1] <= self.y + self.height:
                self.is_open = not self.is_open

        # If the user clicks an option, select it
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_open:
                for i in range(len(self.options)):
                    if self.x <= event.pos[0] <= self.x + self.width and self.y + self.height + i * 20 <= event.pos[
                        1] <= self.y + self.height + i * 20 + 20:
                        self.selected_index = i
                        self.is_open = False

