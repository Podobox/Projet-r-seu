import pygame
import tkinter as tk
from pygame.locals import *

from Controller.Button import Button
from Model.Game import Game
from View.FileMenu import FileMenu
#from View.Visualizer import WINDOW_HEIGHT, WINDOW_WIDTH
pygame.init()
pygame.font.init()


class Barre:

    def __init__(self, window, window_width, window_height, barre_boolean, visualizer):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.barre_boolean = barre_boolean
        self.visualizer = visualizer
        self.game = Game(10000)
        self.money = self.game.get_denarii()
        self.fileButton = Button(self.window, "/Images/file_bouton.png", 0, 2, self.displayFileMenu, 0.25)

    def button(self, panel, mouse):
        # soit 275 la largeur et 30 la hauteur de chaque panel
        if panel.x + panel.width > mouse[0] > panel.x and panel.y + panel.height > mouse[1] > panel.y:
            return True
        else:
            return False

    def barre_function(self, money, population, date):

        global test_file, test
        barre = pygame.image.load('Images/barre.png')
        barre = pygame.transform.scale(barre, (self.window_width, 40))

        font1 = pygame.font.Font(None, 30)
        font2 = pygame.font.Font(None, 25)

        # while self.barre_boolean:
        #global file_click
        self.window.blit(barre, (0, 0))
        """case1=File
        text_file = pygame.image.load('Images/paneling_00010.png')
        self.window.blit(text_file, (10, 10))
        text_file_rect = text_file.get_rect()
        text_file_rect.x = 10
        text_file_rect.y = 10
        text_case1 = font1.render(case1, True, (0, 0, 0))
        self.window.blit(text_case1, (10, 10))"""
        case = pygame.image.load('Images/paneling_00015.png')
        case = pygame.transform.scale(case, (150, 30))


        case2 = "Dn"
        text_case2 = font2.render(case2, True, (255, 255, 255))

        self.window.blit(case, (self.window_width / 3 + 10, 5))
        self.window.blit(text_case2, ((self.window_width / 3) + 20, 10))
        case3 = "Pop"
        text_case3 = font2.render(case3, True, (255, 255, 255))
        self.window.blit(case, (self.window_width / 3 + 200, 5))
        self.window.blit(text_case3, ((self.window_width / 3) + 215, 10))
        self.window.blit(case, (self.window_width / 3 + 450, 5))

        money = str(int(money))
        money = font2.render(money, True, (255, 255, 255))
        self.window.blit(money, ((self.window_width / 3) + 50, 10))
        population = str(population)
        population = font2.render(population, True, (255, 255, 255))
        self.window.blit(population, ((self.window_width / 3) + 250, 10))
        bc = "BC"
        bc = font2.render(bc, True, (255, 255, 0))
        self.window.blit(bc, ((self.window_width / 3) + 540, 10))
        tmp = date.year
        tmp_y = abs(date.year - 341)
        tmp_y = str(tmp_y)
        tmp_y = font2.render(tmp_y, True, (255, 255, 0))
        self.window.blit(tmp_y, ((self.window_width / 3) + 510, 10))
        month_str = date.month
        #month_str = font2.render(month_str, True, (255, 255, 0))
        month_str_set = ["x", "Jan", "Feb", "Mar", "Apr",
                         "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month_str_chosen = font2.render(month_str_set[month_str], True, (255, 255, 0))
        self.window.blit(month_str_chosen, ((self.window_width / 3) + 470, 10))

        self.fileButton.display()

    def displayFileMenu(self):
        self.visualizer.MODE_FILE_MENU = True
        return
