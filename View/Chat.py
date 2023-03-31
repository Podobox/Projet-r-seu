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
        self.message = "Helloo"
        self.input = ""
        self.memory = []
        self.new_input = True
        self.new_message = True
        self.communication = communication
        self.chat = self.creation()
        self.timer = pg.time.get_ticks()
    
    def update(self):
        now = pg.time.get_ticks()
        self.check_input()
        # if a message is sent, send it in peer
        if self.message:
            # self.communication.send(self.message)   
            print("message print: ", self.message)
            self.memory.append(self.message)
            self.new_message = True
            self.message = ""
        if now - self.timer > 4000 and self.memory:
            self.timer = now
            self.memory = self.memory[:-1]

    def display(self, chat):
        chat.update()
        self.display_input()
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
    
    def check_input(self):
        for event in pg.event.get():
                ### deselection the chat ###
                # if (event.type == pg.K_ESCAPE):
                #     running = False
                #     pg.quit()
                #     quit(0)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.input = self.input[:-1]

                    elif event.key == pg.K_RETURN:
                        # add in memory the input
                        self.memory.append(self.input)
                        
                    else:
                        carac = event.dict['unicode']
                        self.input = self.input + carac
                    
                    self.new_input = True

    def display_message(self):
        if self.memory and self.new_message:
            font = pg.font.Font(None, 28)
            text_surface = font.render(self.memory[len(self.memory)-1] , True, (155, 175, 120))
            self.window.blit(text_surface, (self.chat_posx, self.chat_posy-50))
            # self.new_message = False
    def display_input(self):
        if self.input and self.new_input:
            font = pg.font.Font(None, 32)
            text_surface = font.render(self.input, True, (60, 50, 50))
            coordinate = text_surface.get_rect(centery=self.chat.get_rect().centery)
            coordinate.left = 75
            self.chat.blit(text_surface, coordinate)
            # self.window.blit(self.chat, (self.chat_posx, self.chat_posy))
            # self.new_input = False