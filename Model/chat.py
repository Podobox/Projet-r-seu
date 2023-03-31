import pygame
class Chat:
    def __init__(self, window, width, height, font, font_size):
        self.x = window
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
        if len(self.messages) > 10:
            self.messages.pop(0)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)
        font = pygame.font.SysFont(self.font, self.font_size)
        for i, message in enumerate(self.messages):
            text = font.render(message, True, (255, 255, 255))
            surface.blit(text, (self.x + 5, self.y + 5 + i * (self.font_size + 5)))

