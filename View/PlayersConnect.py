import pygame
import Controller.Menu
import sys
class PLayerConnected :
    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height  = window_height
        self.img_posx = window_width -420
        self.img_posy = +97
        
    def display(self):
        # from Controller.Menu import avatar_name
        avatar_image = pygame.image.load(f"./Images/play_menu/{Controller.Menu.avatar_name}.png").convert_alpha()
        avatar_image = pygame.transform.scale(avatar_image, (160, 160))
        avatar_rect = avatar_image.get_rect()
        avatar_rect.topright = (self.img_posx , self.img_posy)

        font = pygame.font.Font(None, 30)
        text = font.render("My Avatar: " + Controller.Menu.avatar_name, True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (self.img_posx - avatar_image.get_width()/2, self.img_posy - 5)
        self.window.blit(avatar_image, avatar_rect)
        self.window.blit(text, text_rect)
        
    def show_players_connected(self, window):
        pygame.font.init()
        new_window = pygame.Surface((800, 500))
        background = pygame.image.load("./Images/back_connected.png").convert_alpha()
        background = pygame.transform.scale(background, new_window.get_size())
        new_window.blit(background, (0, 0))
        new_window_rect = new_window.get_rect(center=window.get_rect().center)
        font = pygame.font.Font(None, 50)
        caption = font.render("Connected Players", True, (255, 0, 0))
        caption_rect = caption.get_rect(center=(new_window.get_width() // 2, new_window.get_height() // 6))
        new_window.blit(caption, caption_rect)
        avatar_images = []
        avatar_names = []  # Liste pour stocker les noms des avatars
        for i in range(len(Controller.Menu.player_list)):
            player = Controller.Menu.player_list[i]
            name = player['avatar']
            avatar_names.append(name)
            avatar_image = pygame.image.load(f"./Images/play_menu/{name}.png").convert_alpha()
            avatar_image = pygame.transform.scale(avatar_image, (100, 100))
            avatar_images.append(avatar_image)

        avatar_positions = []
        for i in range(len(Controller.Menu.player_list)):
            x = new_window.get_width() // (len(Controller.Menu.player_list) + 1) * (i + 1) - 50
            y = new_window.get_height() // 2 - 50
            avatar_positions.append((x, y))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        running = False

          
            for i in range(len(avatar_images)):
                new_window.blit(avatar_images[i], avatar_positions[i])
                font = pygame.font.Font(None, 30)
                text = font.render(avatar_names[i], True, (255, 0, 0))  # Créer un objet texte avec le nom de l'avatar
                text_rect = text.get_rect(center=(avatar_positions[i][0] + 50, avatar_positions[i][1] + avatar_image.get_height() + 10))
                new_window.blit(text, text_rect)

            window.blit(new_window, new_window_rect)
            pygame.display.flip()
