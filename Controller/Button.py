import pygame as pg
import sys, os
from PIL import Image


class Button():


    def __init__(self, window, path, x, y, action, coefficient=1, building=-1, overlay=-1, game=-1, player_avatars=-1):#(self, path, x, y, dx, dy, action):
        self.x = x
        self.y = y
        self.action = action
        self.path = path
        self.overlay = overlay
        self.window = window
        self.coefficient = coefficient
        self.building = building
        self.game = game
        self.player_avatars = player_avatars
        self.obj = self.initObj()

    def display(self):
        self.window.blit(self.obj, (self.x, self.y))

    def initObj(self):
        scriptDir = sys.path[0]
        imagePath = os.path.join(scriptDir + self.path)
        button = pg.image.load(imagePath)

        img = Image.open(imagePath)
        imgWidth = img.width
        imgHeight = img.height

        self.dx = self.x + (imgWidth * self.coefficient + 1)
        self.dy = self.y + (imgHeight * self.coefficient + 1)

        return pg.transform.scale(button, (imgWidth * self.coefficient + 1, imgHeight * self.coefficient + 1))

    def listener_rect(self, pos):
        # dx et dy pour distance y et distance x
        # on retrun true si l'évènement se passe dans le rectangle
        return pos[0] >= self.x and pos[0] <= self.dx and pos[1] >= self.y and pos[1] <= self.dy
