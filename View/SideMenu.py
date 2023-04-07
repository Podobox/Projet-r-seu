import sys
import os
import pygame as pg
from PIL import Image
from Controller.Button import Button
from Model.Road import Road
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.Fountain import Fountain
from Model.Forum import Forum
from Model.Market import Market
from Model.Garden import Garden
from Model.Wheat_Farm import Wheat_Farm
from Model.Senate import Senate
from Model.Granary import Granary
from Model.Well import Well
from Model.House import House
from Model.New_House import New_House
from Model.Map import Map, MAP_DIM

#from Controller.List_Button import list_button


class Menu:

    def __init__(self, window, window_width, window_height, game, isoToCart, visualizer):
        self.window = window
        self.visualizer = visualizer
        self.window_width = window_width
        self.window_height = window_height
        self.game = game
        self.isoToCart = isoToCart

        scriptDir = sys.path[0]
        imagePath = os.path.join(scriptDir + "/Images/play_menu/menu.png")
        self.pannelMenu = pg.image.load(imagePath)

        img = Image.open(imagePath)
        self.imgWidth = img.width
        self.imgHeight = img.height
        self.coefficient = self.window_height / self.imgHeight

        self.pannelMenu = pg.transform.scale(
            self.pannelMenu, (self.imgWidth * self.coefficient, self.window_height))

        variable = self.game.speed
        font = pg.font.Font(None, 30)
        self.speed_print = font.render(str(variable), 1, (255, 255, 255))
        
        self.AddButtons()

        return

    def AddButtons(self):
        self.list_button = [
            Button(self.window, "/Images/play_menu/paneling_00123.png", self.window_width - (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 420), self.action, self.coefficient, New_House),
             Button(self.window, "/Images/Prefecture_00001.png", self.window_width - (self.coefficient *99.26 ),
                   self.window_height - (self.coefficient * 420), self.action, self.coefficient / 1.50, Prefecture),
            Button(self.window, "/Images/EngineerPost_00001.png", self.window_width - (self.coefficient * 49.41),
                   self.window_height - (self.coefficient * 420), self.action, self.coefficient / 1.75, Engineer_Post),

            Button(self.window, "/Images/play_menu/paneling_00135.png", self.window_width - (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 380), self.action, self.coefficient, Road),
            Button(self.window, "/Images/Fountain_00001.png", self.window_width - (self.coefficient
                   * 52), self.window_height - (self.coefficient * 380), self.action, self.coefficient/1.2, Fountain),
            Button(self.window, "/Images/play_menu/paneling_00131.png", self.window_width - (self.coefficient
                   * 99.26), self.window_height - (self.coefficient * 380), self.action, self.coefficient, "destroy"),

            Button(self.window, "/Images/Garden_00001.png", self.window_width - (self.coefficient
                   * 105), self.window_height - (self.coefficient * 340),
                   self.action, self.coefficient/1.5, Garden),
            Button(self.window, "/Images/Forum_00001.png", self.window_width - (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 350),
                   self.action, self.coefficient / 3, Forum),
            Button(self.window, "/Images/Granary_00001.png", self.window_width - (self.coefficient
                   * 35), self.window_height - (self.coefficient * 350),
                   self.action, self.coefficient / 4, Granary),
            Button(self.window, "/Images/Well_00001.png", self.window_width -
                   (self.coefficient
                   * 65), self.window_height - (self.coefficient * 345), self.action,
                   self.coefficient / 2, Well),

            Button(self.window, "/Images/Market_00001.png", self.window_width -
                   (self.coefficient
                   * 99.26), self.window_height - (self.coefficient * 305), self.action,
                   self.coefficient / 2.5, Market),
            Button(self.window, "/Images/Farm_00001.png", self.window_width - (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 305),
                   self.action, self.coefficient / 2.5, Wheat_Farm),
            Button(self.window, "/Images/Senate_00001.png", self.window_width - (self.coefficient
                   * 49.41), self.window_height - (self.coefficient * 310), self.action,
                   self.coefficient / 5.5, Senate),

            Button(self.window, "/Images/play_menu/paneling_00247.png", self.window_width - (self.coefficient
                   * 49.41), self.window_height - (self.coefficient * 60), self.game.increase_speed, self.coefficient),
            Button(self.window, "/Images/play_menu/paneling_00251.png", self.window_width - (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 60), self.game.decrease_speed, self.coefficient),
            Button(self.window, "/Images/play_menu/paneling_001631.png", self.window_width - (self.coefficient
                   * 99.26), self.window_height - (self.coefficient * 60), self.game.pause, self.coefficient),

            Button(self.window, "/Images/show_map.png", self.window_width -
                   (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 270), self.changeOverlay,
                   self.coefficient / 5, overlay=None),
            Button(self.window, "/Images/show_grid.png", self.window_width -
                   (self.coefficient
                   * 80), self.window_height - (self.coefficient * 270), self.showGrid,
                   self.coefficient / 5),
            Button(self.window, "/Images/collapse_overlay.png", self.window_width -
                   (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 240), self.changeOverlay,
                   self.coefficient / 10.5, overlay="Damage"),
            Button(self.window, "/Images/fire_overlay.png", self.window_width -
                   (self.coefficient
                   * 80), self.window_height - (self.coefficient * 240), self.changeOverlay,
                   self.coefficient / 10.5, overlay="Fire"),
            Button(self.window, "/Images/water_overlay.png", self.window_width -
                   (self.coefficient
                   * 149.117), self.window_height - (self.coefficient * 220), self.changeOverlay,
                   self.coefficient / 10.5, overlay="Water"),
            Button(self.window, "/Images/Show_Tile.png", self.window_width -
            (self.coefficient
            * 158.117), self.window_height - (self.coefficient * 25), self.changeOverlay,
            self.coefficient /9.5, overlay="Tile"),
            Button(self.window, "/Images/Connected_Player.png", self.window_width - 300 , self.window_height-1040 , self.changeOverlay,
            self.coefficient /9.5, "show_players"),
    
            Button(self.window, "/Images/desirability_overlay.png", self.window_width -
                   (self.coefficient
                   * 80), self.window_height - (self.coefficient * 220), self.changeOverlay,
                   self.coefficient / 10.5, overlay="Desirability")


        ]

    def display(self):
        font = pg.font.Font(None, 30)
        self.speed_print = font.render("speed : "+str(int(self.game.speed*100))+"%", 1, (0, 0, 0))
        
        self.window.blit(self.pannelMenu, (self.window_width-(self.imgWidth*self.coefficient),0))

        self.window.blit(self.speed_print, (self.window_width-200,self.window_height-50))

        for button in self.list_button:
            button.display()
        return self.list_button

    def action(self, building, init_pos, final_pos):
        init_pos = self.isoToCart(init_pos)
        final_pos = self.isoToCart(final_pos)
        #print("positions sur la carte : ", final_pos, init_pos)
        if final_pos[0] >= MAP_DIM or final_pos[1] >= MAP_DIM or init_pos[0] >= MAP_DIM or init_pos[1] >= MAP_DIM:
            return

        if final_pos[0] < 0 or final_pos[1] < 0 or init_pos[0] < 0 or init_pos[1] < 0:
            return

        if building == Senate :
            self.game.build(init_pos[1], init_pos[0], building)
            return
        
        if building == Wheat_Farm :
            self.game.build(init_pos[1], init_pos[0], building)
            return
        
        if(final_pos == init_pos):
            if building == "destroy":
                self.game.destroy(final_pos[1], final_pos[0])
            else:
                self.game.build(final_pos[1], final_pos[0], building)
        


        if init_pos[0] <= final_pos[0]:
            mini_x = init_pos[0]
            max_x = final_pos[0]
        else:
            mini_x = final_pos[0]
            max_x = init_pos[0]

        if init_pos[1] <= final_pos[1]:
            mini_y = init_pos[1]
            max_y = final_pos[1]
        else:
            mini_y = final_pos[1]
            max_y = init_pos[1]

        old_mini_x = mini_x
        while mini_y <= max_y:
            while mini_x <= max_x:
                if building == "destroy":
                    self.game.destroy(mini_y, mini_x)
                else:
                    self.game.build(mini_y, mini_x, building)
                mini_x += 1
            mini_x = old_mini_x
            mini_y+=1
        return


    def changeOverlay(self, option):
        self.visualizer.overlayType=option
        return
    

    def showGrid(self):
        self.visualizer.showGrid= not self.visualizer.showGrid 
        return
