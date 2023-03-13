from operator import imod
from turtle import window_width
import pygame as pg
import tkinter as tk
from Model.Engineer_Post import Engineer_Post
from Model.Farm import Farm
from Model.Forum import Forum
from Model.Fountain import Fountain
from Model.Garden import Garden
from Model.House import House
from Model.Map import Map, MAP_DIM
import Images as img
import sys
import os
from Model.Market import Market
from Model.New_House import New_House
from Model.Prefecture import Prefecture
from Model.Road import Road
from Model.Collapsed import Collapsed
from random import randint
from PIL import Image
from Controller.Button import Button
from Model.Senate import Senate
from Model.Well import Well
from Model.Wheat_Farm import Wheat_Farm
from View.SideMenu import Menu
from Model.Road import Road
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.House import House
from Model.Granary import Granary
from Model.Water import Water
from Model.Tree import Tree
from Model.Rock import Rock
from Model.Other_Rock import Other_Rock


class Minimap:
        
    coefficient = 7 #8 pour 162.5 #faire coefficient en passant à 8 et l'appliquer sur 100

    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.minimap_posx = (window_width-340)
        self.minimap_posy = (window_height-475)
        self.width = self.coefficient*30
        self.height = self.coefficient*30
        


    def update(self, map):
        self.minimap = pg.Surface((self.width, self.height))
        for x in range(MAP_DIM):
                    for y in range(MAP_DIM):
                        match map.grid[x][y].building:
                            case House():
                                pg.draw.rect(self.minimap, (153, 153, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Prefecture():
                                pg.draw.rect(self.minimap, (255, 0, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Road():
                                pg.draw.rect(self.minimap, (144, 110, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Collapsed():
                                pg.draw.rect(self.minimap, (141, 141, 141), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Engineer_Post():
                                pg.draw.rect(self.minimap, (255, 255, 255), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case New_House():
                                pg.draw.rect(self.minimap, (153, 153, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Fountain():
                                pg.draw.rect(self.minimap, (96, 106, 196), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Garden():
                                pg.draw.rect(self.minimap, (0, 155, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Forum():
                                pg.draw.rect(self.minimap, (255, 255, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Granary():
                                pg.draw.rect(self.minimap, (153, 0, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Market():
                                pg.draw.rect(self.minimap, (255, 0, 127), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Wheat_Farm():
                                pg.draw.rect(self.minimap, (255, 128, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Farm():
                                pg.draw.rect(self.minimap, (255, 128, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Senate():
                                pg.draw.rect(self.minimap, (0, 255, 255), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Well():
                                pg.draw.rect(self.minimap, (51, 153, 255), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Water():
                                pg.draw.rect(self.minimap, (0, 0, 255), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Tree():
                                pg.draw.rect(self.minimap, (0, 255, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case Rock():
                                pg.draw.rect(self.minimap, (192, 192, 192), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))

                            case Other_Rock():
                                pg.draw.rect(self.minimap, (192, 192, 192), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))
                            
                            case None:
                                pg.draw.rect(self.minimap, (0, 255, 0), (y*self.coefficient, x*self.coefficient, self.coefficient, self.coefficient))


    
    def display(self, map, deplacementX, deplacementY):
        self.update(map)
        self.minimap.set_at((0,0), (0,0,0))
        self.minimap = pg.transform.rotate(self.minimap, -45)


        self.window.blit(self.minimap, (self.minimap_posx, self.minimap_posy))
        
        self.minimap = None
        return