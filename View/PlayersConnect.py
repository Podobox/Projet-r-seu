import pygame
import Controller.Menu

class PLayerConnected :
    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height  = window_height
        self.img_posx = window_width -400
        self.img_posy = +60
        
    def display(self):
        # from Controller.Menu import avatar_name
        avatar_image = pygame.image.load(f"./Images/play_menu/{Controller.Menu.avatar_name}.png").convert_alpha()
        avatar_image = pygame.transform.scale(avatar_image, (100, 100))
        avatar_rect = avatar_image.get_rect()
        avatar_rect.topright = (self.img_posx , self.img_posy)

        font = pygame.font.Font(None, 30)
        text = font.render(Controller.Menu.avatar_name, True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.img_posx - avatar_image.get_width()/2, self.img_posy - 5)
        self.window.blit(avatar_image, avatar_rect)
        self.window.blit(text, text_rect)
