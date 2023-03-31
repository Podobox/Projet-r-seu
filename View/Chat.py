import pygame as pg
from Controller.Communication import Communication
class Chat:

    def __init__(self, window, window_width, window_height, communication):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.width = 300
        self.height = 40
        self.chat_posx = 40
        self.chat_posy = window_height - 100
        self.message = "Hello"
        self.memory = []
        self.communication = communication
        self.chat = self.creation()
        self.timer = pg.time.get_ticks()
    
    def update(self):
        now = pg.time.get_ticks()
        # self.chat.fill((150, 200, 200))
        # self.check_chat()
        # if a message is sent, send it in peer
        if self.message:
            # self.communication.send(self.message)   
            print("message print: ", self.message)
            self.memory.append(self.message)
            self.message = ""
        if now - self.timer > 4000 and self.memory:
            self.timer = now
            self.memory = self.memory[:-1]

    def display(self, chat):
        chat.update()
        self.display_message()
        self.window.blit(self.chat, (self.chat_posx, self.chat_posy))

    def creation(self):
        c = pg.Surface((self.width, self.height))
        c.fill((150, 200, 200))
        # add text inside
        font = pg.font.Font(None, 36)
        text_surface = font.render("Chat:", True, (40, 40, 40))
        coordinate = text_surface.get_rect(center=c.get_rect().center)
        coordinate.x -= 115
        c.blit(text_surface, coordinate)
        return c
    
    def check_chat(self):
        for event in pg.event.get():
                if (event.type == pg.K_ESCAPE):
                    running = False
                    pg.quit()
                    quit(0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        nom = nom[:-1]
                        screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                        #supp_text= pg.image.load("Images/supp_text.png")
                        text_2 = font.render(nom, True, (0, 0, 0))
                        screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                        pg.display.flip()
                    elif event.key == pg.K_RETURN:
                        # display the text input on the screen
                        pass
                        
                    else:
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_ESCAPE:
                                pg.quit()
                                quit(0)
                        carac = event.dict['unicode']
                        nom = nom + carac
                        text_2 = font.render(nom, True, (0, 0, 0))
                        screen.blit(zone_de_texte, ((x[0] / 2) - 150, (x[1] / 3) + 50))
                        screen.blit(text_2, (x[0] / 2 - 100, (x[1] / 3) + 70))
                        pg.display.flip()
    def display_message(self):
        if self.memory:
            font = pg.font.Font(None, 28)
            text_surface = font.render(self.memory[len(self.memory)-1] , True, (155, 175, 120))
            self.window.blit(text_surface, (self.chat_posx, self.chat_posy-50))