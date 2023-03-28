import pygame as pg

class Chat:

    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.chat_posx = (350)
        self.chat_posy = (270)
    
    def display(self, map, deplacementX, deplacementY):
        self.update(map)
        self.minimap.set_at((0,0), (0,0,0))
        self.minimap = pg.transform.rotate(self.minimap, -45)


        self.window.blit(self.minimap, (self.minimap_posx, self.minimap_posy))
        
        self.minimap = None
        return