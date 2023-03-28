import random

from Model.Player import Player
from Model.Grass import Grass
from Model.Map import MAP_DIM
from Model.Other_Rock import Other_Rock
from Model.Rock import Rock
from Model.Tree import Tree
from Model.Water import Water
from View.Visualizer import Visualizer, cellSizeDict
from Model.Game import Game
from Model.House import House
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.Road import Road
from Model.Senate import Senate
from Model.Collapsed import Collapsed
from Model.Well import Well
from Model.Fountain import Fountain
from Model.Wheat_Farm import Wheat_Farm
from Model.Market import Market
from Model.Garden import Garden
from Model.Granary import Granary
import pygame as pg
from Model.Forum import Forum
from Model.New_House import New_House
from datetime import date, timedelta
from time import time_ns, sleep
from Controller.Backup import Backup
from Model.Destination_Walkers import Destination_Walkers
from random import randint
from Controller.Communication import Communication

FRAMES_PER_SECONDS = 7
TIME_NS_PER_FRAME = 1 / FRAMES_PER_SECONDS * 1e9


class Controller:

    MODE_DECALAGE = False
    MODE_BUILD = False
    building = False
    init_pos = None
    final_pos = None
    ORIGIN_DECALAGE = (0, 0)

    def __init__(self, name_save, game=None, players=None):
        # pg.init()
        self.list_button = []
        self.MODE_DECALAGE = False
        self.ORIGIN_DECALAGE = (0, 0)
        # game is actually always set so changing the money here won't do anything
        self.game = Game(100000) if game is None else game
        self.backup = Backup(name_save)
        self.communication = Communication()
        self.visualizer = Visualizer(self.list_button, self.game, self.backup, self.communication)
        self.building = False
        self.buttonclicked = None
        self.last_frame = time_ns()
        self.player = Player()
        self.players = players
        if self.players is None:
            self.game.take_all_ownership(self.player)

        # Benchmarking
        # self.bench = 0
        # self.bench_nb = 0
        self.run()

    def run(self):
        # print(self.game)
        # d = Destination_Walkers(self.game.map, self.game.map.grid[1][1].building)
        for _ in range(5):
            self.game.increase_speed()

        self.game.build(15, 15, Prefecture)

        while True:
            self.game.advance_time()

            self.game.job_hunt()
            self.game.burn()
            self.game.collapse()
            self.game.compute_desirability()
            self.game.map.compute_water_coverage()
            self.game.check_evolution()
            self.game.eat()
            self.game.farm()
            self.game.walk()
            self.game.fill_market()
            self.game.engineer()
            self.game.firefight()
            self.game.collect_tax()
            self.game.trade_market()

            self.list_button = self.visualizer.update(self.game.map, self.game.walkers)

            pg.display.update()

            # for message in self.communication.check_messages():
            #     self.handle_message()

            self.wait_next_frame()

            self.checkEvents()

        print(self.game)
        return

    def handle_message(self):
        # logic here, call functions from self.communication to actually send the answer
        pass

    def wait_next_frame(self):
        time_now = time_ns()
        delta = time_now - self.last_frame
        sleep_time = TIME_NS_PER_FRAME - delta if TIME_NS_PER_FRAME - delta > 0 else 0
        # Benchmarking
        # self.bench = (sleep_time * 1e-9 + self.bench * self.bench_nb) \
            # / (self.bench_nb + 1)
        # instant_bench = ((TIME_NS_PER_FRAME - sleep_time) / TIME_NS_PER_FRAME * 100)
        # self.bench = (((TIME_NS_PER_FRAME - sleep_time) / TIME_NS_PER_FRAME * 100)
        # + self.bench * self.bench_nb) / (self.bench_nb + 1)
        # self.bench_nb += 1
        # print(self.bench)
        # print(instant_bench)
        # print(sleep_time * 1e-9)
        # sleep(sleep_time * 1e-9)
        # instant_bench = ((TIME_NS_PER_FRAME - sleep_time) / TIME_NS_PER_FRAME * 100)
        # print(instant_bench)

        # No more useless sleeping
        self.checkEvents(sleep_time)
        self.last_frame = time_ns()

    def checkEvents(self, delta_time=0):
        stop_time = time_ns() + delta_time
        for event in pg.event.get():

            if time_ns() >= stop_time:
                return
            match event.type:
                case pg.QUIT:
                    print("Trying to exit...")
                    pg.quit()
                    exit()
                case pg.KEYDOWN:
                    print("Pressed ", event.unicode)
                case pg.KEYUP:
                    print("Released ", event.unicode)
                case pg.MOUSEBUTTONDOWN:
                    print("MouseButtonDown")
                    if event.button == pg.BUTTON_LEFT:
                        print("Left button pressed at (x, y) = ", event.pos)

                        print("self.building est a : ", self.building)
                        # ------------------------------------------------------------------------------------Faire en clique droit
                    elif event.button == pg.BUTTON_RIGHT:
                        print("Right button pressed at (x, y) = ", event.pos)
                        if event.pos[0] <= self.visualizer.GAME_WIDTH and event.pos[1] <= self.visualizer.GAME_HEIGHT:
                            self.MODE_DECALAGE = True
                            self.ORIGIN_DECALAGE = event.pos

                case pg.MOUSEBUTTONUP:
                    if event.button == pg.BUTTON_LEFT:
                        if self.MODE_BUILD:
                            # --------------------------------------Appeler la fonction pour ajouter en rectangle mode
                            self.final_pos = event.pos
                            self.buttonclicked.action(
                                self.buttonclicked.building, self.init_pos, self.final_pos)
                            self.MODE_BUILD = False
                            self.building = False
                            self.visualizer.changeBuildingMode()
                            self.final_pos = None
                        print("Left button released at (x, y) = ", event.pos)
                    elif event.button == pg.BUTTON_RIGHT:
                        print("Right button released at (x, y) = ", event.pos)
                        if self.MODE_DECALAGE:
                            self.MODE_DECALAGE = False
                            mouse_pos = event.pos
                            self.visualizer.tmpDeplacementX = mouse_pos[0] - self.ORIGIN_DECALAGE[0]
                            self.visualizer.tmpDeplacementY = mouse_pos[1] - self.ORIGIN_DECALAGE[1]
                            self.visualizer.deplacementX += self.visualizer.tmpDeplacementX
                            self.visualizer.deplacementY += self.visualizer.tmpDeplacementY
                            self.visualizer.tmpDeplacementX = 0
                            self.visualizer.tmpDeplacementY = 0
                case pg.MOUSEMOTION:
                    if event.type == pg.MOUSEMOTION:
                        if self.MODE_BUILD:
                            self.visualizer.changeBuildingMode(
                                self.buttonclicked, self.init_pos, event.pos)
                        elif self.building:
                            self.visualizer.changeBuildingMode(self.buttonclicked, event.pos)
                            # print("position de la souris : ", event.pos)
                        if self.MODE_DECALAGE:
                            # self.MODE_DECALAGE = False
                            mouse_pos = event.pos
                            self.visualizer.tmpDeplacementX = mouse_pos[0] - self.ORIGIN_DECALAGE[0]
                            self.visualizer.tmpDeplacementY = mouse_pos[1] - self.ORIGIN_DECALAGE[1]
                case pg.MOUSEWHEEL:
                    if not self.MODE_DECALAGE and event.y != 0:
                        if event.y > 0:
                            # zoom in
                            new_zoom_percentage = max(cellSizeDict.keys())
                            for zoom_percentage in cellSizeDict.keys():
                                if zoom_percentage > self.visualizer.zoom and zoom_percentage < new_zoom_percentage:
                                    new_zoom_percentage = zoom_percentage
                            if new_zoom_percentage != self.visualizer.zoom:
                                self.visualizer.deplacementX = self.visualizer.deplacementX * new_zoom_percentage / self.visualizer.zoom
                                self.visualizer.deplacementY = self.visualizer.deplacementY * new_zoom_percentage / self.visualizer.zoom
                        else:
                            # zoom out
                            new_zoom_percentage = min(cellSizeDict.keys())
                            for zoom_percentage in cellSizeDict.keys():
                                if zoom_percentage < self.visualizer.zoom and zoom_percentage > new_zoom_percentage:
                                    new_zoom_percentage = zoom_percentage
                            if new_zoom_percentage != self.visualizer.zoom:
                                # self.visualizer.deplacementX += self.visualizer.GAME_WIDTH / 4
                                # self.visualizer.deplacementY += self.visualizer.GAME_HEIGHT / 4
                                self.visualizer.deplacementX *= new_zoom_percentage
                                self.visualizer.deplacementY *= new_zoom_percentage
                                self.visualizer.deplacementX /= self.visualizer.zoom
                                self.visualizer.deplacementY /= self.visualizer.zoom
                        self.visualizer.zoom = new_zoom_percentage
                case _:
                    # print(pg.event.event_name(event.type), "occured")
                    mouse_button_pressed = pg.mouse.get_pressed()
                    left_button_pressed = mouse_button_pressed[0]
                    right_button_pressed = mouse_button_pressed[2]
                    mouse_pos = pg.mouse.get_pos()
                    if right_button_pressed:
                        if mouse_pos[0] <= self.visualizer.GAME_WIDTH and mouse_pos[1] <= self.visualizer.GAME_HEIGHT:
                            self.MODE_DECALAGE = True
                            self.ORIGIN_DECALAGE = mouse_pos
                    if left_button_pressed:
                        actionned = False
                        if not(self.building):
                            print("into not(self.building)")
                            for button in self.list_button:
                                if button.listener_rect(mouse_pos):
                                    print("button clicked")
                                    self.buttonclicked = button

                                    if self.buttonclicked.building != -1:
                                        self.building = True
                                    elif self.buttonclicked.overlay != -1:
                                        self.buttonclicked.action(self.buttonclicked.overlay)

                                    elif self.buttonclicked.game != -1:
                                        self.buttonclicked.action(self.buttonclicked.game)

                                    else:
                                        self.buttonclicked.action()
                                        actionned = True

                                    break
                        else:
                            self.init_pos = mouse_pos
                            self.MODE_BUILD = True

                        if self.visualizer.MODE_FILE_MENU and not actionned:
                            self.visualizer.MODE_FILE_MENU = False
                    break
