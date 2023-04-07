import sys
import os
import pygame as pg
from PIL import Image
from Controller.Button import Button
from Model.Road import Road
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.House import House
from Controller.Backup import Backup
import Controller.Communication as com
from Model.Map import MAP_DIM


class FileMenu:

    def __init__(self, window, window_width, window_height, backup, game):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.coefficient = 0.28
        self.backup = backup
        self.game = game

        self.AddButtons()

        return

    # Button(self, path, x, y, dx, dy, action):
    def AddButtons(self):
        # Boutons de la liste file: load & game
        self.list_button = [
            #Button(self.window, "/Images/load_game2.png",0, 42, self.backup.load(), self.coefficient, ),
            Button(self.window, "/Images/save_game2.png", 0, 42,
                   self.backup.save, self.coefficient, game=self.game),
            Button(self.window, "/Images/exit_game.png", 0, 83.5, self.quit, self.coefficient)

        ]

    def display(self):
        for button in self.list_button:
            button.display()
        return self.list_button

    def quit(self):
        for x in range(MAP_DIM):
            for y in range(MAP_DIM):
                if self.game.map.grid[x][y].owner is not None:
                    com.communication.disconnect(x, y)
        exit()
        return

    def action(self):
        print("clicked")
        return

    def action1(self):
        Backup.load(self)

    def action2(self):
        Backup.save(self)
