import pygame as pg
from Controller.Communication import Communication

FONT = pg.font.Font(None, 32)
FONT2 = pg.font.Font(None, 28)
class Chat:

    def __init__(self, window, window_width, window_height, communication):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.width = 300
        self.height = 40
        self.chat_posx = 40
        self.chat_posy = window_height - 100
        self.message = ""
        self.input = ""
        self.memory = []
        # boolean to know when refresh screen
        self.new_input = True

        self.communication = communication
        self.chat = self.creation()
    
    def update(self, now):
        self.check_input(now)
        # if a message is sent, send it in peer to everyone and add it in memory
        if self.message:
            # self.communication.send(self.message)   
            print("message print: ", self.message)
            self.memory.append((self.message, pg.time.get_ticks()))
            print("Voici la mémoire", self.memory)
            self.message = ""

        if self.memory and now - self.memory[0][1] > 4000 :
            self.memory = self.memory[1:]
            

    def display(self, chat):
        now = pg.time.get_ticks()
        chat.update(now)
        self.display_message(now)
        self.display_input()
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
    
    def check_input(self, now):
        for event in pg.event.get():
                ### deselection the chat ###
                # if (event.type == pg.K_ESCAPE):
                #     running = False
                #     pg.quit()
                #     quit(0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.input = self.input[:-1]

                    elif event.key == pg.K_RETURN and self.input:
                        self.message = self.input
                        self.input = ""
                        self.chat = self.creation()
                        
                    else:
                        carac = event.dict['unicode']
                        # don't input the key enter in carac
                        if carac != '\r':
                            self.input = self.input + carac
                    
                    # self.new_input = True

    def display_message(self, now):
        if self.memory: 
            # if there's just one word in memory
            if len(self.memory) == 1:
                text_surface = FONT2.render(self.memory[0][0] , True, (155, 175, 120))
                if now - self.memory[0][1] > 2000:
                    t = int(255*(2-(now - self.memory[0][1]) / 2000))
                    text_surface.set_alpha(t)
                elif now - self.memory[0][1] > 4000:
                    t = 0
                self.window.blit(text_surface, (self.chat_posx, self.chat_posy-40))
            else:
                for i in range(len(self.memory)):
                    text_surface = FONT2.render(self.memory[len(self.memory)-1-i][0] , True, (155, 175, 120))
                    # add the transparency on the text
                    if now - self.memory[len(self.memory)-1-i][1] > 2000:
                        t = int(255*(2-(now - self.memory[len(self.memory)-1-i][1]) / 2000))
                        text_surface.set_alpha(t)
                    elif now - self.memory[len(self.memory)-1-i][1] >= 4000:
                        t = 0
                        text_surface.set_alpha(t)
                    self.window.blit(text_surface, (self.chat_posx, self.chat_posy-40*(i+1)))
    def display_input(self):
        if self.input and self.new_input:
            text_surface = FONT.render(self.input, True, (60, 50, 50))
            coordinate = text_surface.get_rect(centery=self.chat.get_rect().centery)
            coordinate.left = 75
            self.chat.blit(text_surface, coordinate)
            # self.window.blit(self.chat, (self.chat_posx, self.chat_posy))
            # self.new_input = False
    