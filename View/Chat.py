import pygame as pg
from Controller.Communication import Communication
import enum

# text to print
FONT = pg.font.Font(None, 32)
FONT2 = pg.font.Font(None, 28)

class Letter(enum.Enum):
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26


def convert_letter(letter):
    match letter:
        case 'a':
            return 1
        case 'b':
            return 2
        case 'c':
            return 3
        case 'd':
            return 4
        case 'e':
            return 5
        case 'f':
            return 6
        case 'g':
            return 7
        case 'h':
            return 8
        case 'i':
            return 9
        case 'j':
            return 10
        case 'k':
            return 11
        case 'l':
            return 12
        case 'm':
            return 13
        case 'n':
            return 14
        case 'o':
            return 15
        case 'p':
            return 16
        case 'q':
            return 17
        case 'r':
            return 18
        case 's':
            return 19
        case 't':
            return 20
        case 'u':
            return 21
        case 'v':
            return 22
        case 'w':
            return 23
        case 'x':
            return 24
        case 'y':
            return 25
        case 'z':
            return 26
        case _:
            return 27


def convert_number(number):
    match number:
        case 1:
            return 'a'
        case 2:
            return 'b'
        case 3:
            return 'c'
        case 4:
            return 'd'
        case 5:
            return 'e'
        case 6:
            return 'f'
        case 7:
            return 'g'
        case 8:
            return 'h'
        case 9:
            return 'i'
        case 10:
            return 'j'
        case 11:
            return 'k'
        case 12:
            return 'l'
        case 13:
            return 'm'
        case 14:
            return 'n'
        case 15:
            return 'o'
        case 16:
            return 'p'
        case 17:
            return 'q'
        case 18:
            return 'r'
        case 19:
            return 's'
        case 20:
            return 't'
        case 21:
            return 'u'
        case 22:
            return 'v'
        case 23:
            return 'w'
        case 24:
            return 'x'
        case 25:
            return 'y'
        case 26:
            return 'z'
        case _:
            return '?'


def convert_msg(message):
    new_msg = 0
    for w in message:
        new_msg += f'{convert_letter(w)}0'
    return int(new_msg[:-1])


def convert_receive_msg(number):
    msg = ""
    return msg


class Chat:

    def __init__(self, window, window_width, window_height, communication):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.width = 300
        self.height = 40
        self.chat_posx = 40
        self.chat_posy = window_height - 100
        self.receive_msg = 0
        self.len_receive_message = 0
        self.message = ""
        self.input = ""
        self.memory = []
        # boolean to know when refresh screen
        self.new_input = True
        self.is_selected = False
        self.communication = communication
        self.chat = self.creation()
        self.chat_selected = self.creation_selected()

    def update(self, now):
        mouse_pos = pg.mouse.get_pos()
        mouse_button_pressed = pg.mouse.get_pressed()

        if mouse_button_pressed[0]:
            if (self.chat_posx <= mouse_pos[0] <= self.chat_posx + self.chat.get_width()) and (
                    self.chat_posy <= mouse_pos[1] <= self.chat_posy + self.chat.get_height()):
                self.is_selected = True
            else:
                self.is_selected = False
        if self.is_selected:
            self.check_input(now)
        # can take control of chat with enter key
        else:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.is_selected = True

        # receive messages from others
        if self.receive_msg and not self.message:
            self.message = convert_receive_msg(self.receive_msg)

        # if a message is sent, send it in peer to everyone and add it in memory
        if self.message:
            self.communication.send_chat_message(self.message)
            self.memory.append((self.message, pg.time.get_ticks()))
            self.message = ""

        if self.memory and now - self.memory[0][1] > 4000:
            self.memory = self.memory[1:]

    def display(self, chat):
        now = pg.time.get_ticks()
        chat.update(now)
        self.display_message(now)
        self.display_input()
        if self.is_selected:
            self.window.blit(self.chat_selected, (self.chat_posx - 4, self.chat_posy - 2))
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

    def creation_selected(self):
        c = pg.Surface((self.width + 8, self.height + 4))
        c.fill((180, 200, 200))
        return c

    def check_input(self, now):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    self.input = self.input[:-1]
                    self.chat = self.creation()

                elif event.key == pg.K_ESCAPE:
                    self.is_selected = False

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
                text_surface = FONT2.render(self.memory[0][0], True, (155, 175, 120))
                if now - self.memory[0][1] > 2000:
                    t = int(255 * (2 - (now - self.memory[0][1]) / 2000))
                    text_surface.set_alpha(t)
                elif now - self.memory[0][1] > 4000:
                    t = 0
                self.window.blit(text_surface, (self.chat_posx, self.chat_posy - 40))
            else:
                for i in range(len(self.memory)):
                    text_surface = FONT2.render(self.memory[len(self.memory) - 1 - i][0], True, (155, 175, 120))
                    # add the transparency on the text
                    if now - self.memory[len(self.memory) - 1 - i][1] > 2000:
                        t = int(255 * (2 - (now - self.memory[len(self.memory) - 1 - i][1]) / 2000))
                        text_surface.set_alpha(t)
                    elif now - self.memory[len(self.memory) - 1 - i][1] >= 4000:
                        t = 0
                        text_surface.set_alpha(t)
                    self.window.blit(text_surface, (self.chat_posx, self.chat_posy - 40 * (i + 1)))

    def display_input(self):
        if self.input and self.new_input:
            text_surface = FONT.render(self.input, True, (60, 50, 50))
            coordinate = text_surface.get_rect(centery=self.chat.get_rect().centery)
            coordinate.left = 75
            self.chat.blit(text_surface, coordinate)
            # self.window.blit(self.chat, (self.chat_posx, self.chat_posy))
            # self.new_input = False


