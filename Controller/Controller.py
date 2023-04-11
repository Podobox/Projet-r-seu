import random
import subprocess
import os
from Model.Player import Player
from Model.Grass import Grass
from Model.Map import MAP_DIM
from Model.Other_Rock import Other_Rock
from Model.Rock import Rock
from Model.Tree import Tree
from Model.Water import Water
from View.Visualizer import Visualizer, cellSizeDict
from Model.Game import Game, building_type, walker_type
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
from Controller.Communication import Communication, MessageType
import Controller.Communication as com
from Model.Farm_Boy import Farm_Boy_State, Farm_Boy
from Model.Market_Buyer import Market_Buyer_State, Market_Buyer
from Model.Market_Trader import Market_Trader
from Model.Migrant import Migrant
from Model.Engineer import Engineer
from Model.Prefect import Prefect
from Model.Tax_Collector import Tax_Collector
from Model.Walkers import Direction
from Model.Building import STAGES_BEFORE_BURN, STAGES_BEFORE_COLLAPSE

FRAMES_PER_SECONDS = 10
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
        self.player = Player()
        self.players = players
        com.ME = self.player
        self.list_button = []
        self.MODE_DECALAGE = False
        self.ORIGIN_DECALAGE = (0, 0)
        # game is actually always set so changing the money here won't do anything
        self.game = Game(100000) if game is None else game
        self.backup = Backup(name_save)
        if players is None:
            self.game.take_all_ownership(self.player)
        self.game.set_initial_map()
        self.visualizer = Visualizer(self.list_button, self.game, self.backup)
        self.building = False
        self.buttonclicked = None
        self.last_frame = time_ns()

        # Benchmarking
        self.bench = 0
        self.bench_nb = 0
        # self.communication = Communication()
        self.checkDaemon()
        self.run()


    def run(self):
        # print(self.game)
        # d = Destination_Walkers(self.game.map, self.game.map.grid[1][1].building)
        for _ in range(5):
            self.game.increase_speed()

        # for x in range(MAP_DIM):
        #     for y in range(MAP_DIM):
        #         print(self.game.map.grid[x][y].owner)
        # for x in range(10, 15):
            # for y in range(2, 20):
                # self.game.destroy(x, y)

        # for x in range(13, 15):
            # for y in range(2, 8):
                # self.game.build(x, y, New_House)
        # for x in range(13, 15):
            # for y in range(2, 8):
                # self.game.map.grid[x][y].owner = None
        # for x in range(0, 20):
            # for y in range(1):
                # self.game.map.grid[x][y].owner = None
        for x in range(MAP_DIM):
            for y in range(MAP_DIM):
                self.game.map.grid[x][y].owner = None

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

            for message in com.communication.check_messages():
                self.handle_message(message)

            self.wait_next_frame()

            self.checkEvents()

        print(self.game)
        return

    def handle_message(self, message):
        print(f"received {message}")
        match MessageType(message[0]):
            case MessageType.REQUIRE_OWNERSHIP:
                if self.game.map.grid[message[1]][message[2]].owner == com.ME:
                    self.game.map.grid[message[1]][message[2]] = None
                    com.communication.give_ownership(message[1], message[2], message[3])
            case MessageType.GIVE_OWNERSHIP:
                # not handled here
                pass
            case MessageType.CONNECT:
                Backup("online_game").save(self.game)
                com.communication.accept_connect()
            case MessageType.DISCONNECT:
                # message sent only to me, i take all the tiles
                self.game.map.grid[message[1]][message[2]].owner = com.ME
            case MessageType.ACCEPT_CONNECTION:
                pass
            case MessageType.CHANGE_OWNERSHIP:
                # not necessary
                pass
            case MessageType.BUILD:
                self.game.build(message[1], message[2],
                                building_type(message[3], to_num=False), force=True)
            case MessageType.DESTROY:
                self.game.destroy(message[1], message[2], force=True)
            case MessageType.CATCH_FIRE:
                self.game.map.grid[message[1]][message[2]].building.catch_fire(
                    self.game.date)
            case MessageType.PUT_OUT_FIRE:
                self.game.map.grid[message[1]][message[2]].building.put_out_fire(
                    self.game.date)
            case MessageType.EVOLVE:
                self.game.map.grid[message[1]][message[2]].building.evolve()
            case MessageType.DEVOLVE:
                self.game.map.grid[message[1]][message[2]].building.devolve()
            case MessageType.MOVE_WALKER:
                # TODO never called
                b = self.game.map.grid[message[1]][message[2]].building
                w = None
                t = walker_type(message[3], to_num=False)
                if t == Engineer: w = b.engineer
                elif t == Farm_Boy: w = b.farm_boy
                elif t == Market_Buyer: w = b.buyer
                elif t == Market_Trader: w = b.trader
                elif t == Migrant: w = b.migrant
                elif t == Prefect: w = b.prefect
                elif t == Tax_Collector: w = b.tax_collector
                w.direction = Direction(message[4])
            case MessageType.REQUIRE_MONEY_OWNERSHIP:
                pass
            case MessageType.REQUIRE_POPULATION_OWNERSHIP:
                pass
            case MessageType.BURN_STAGE_INCREASE:
                # message is (posx, posy, burn_stage)
                b = self.game.map.grid[message[1]][message[2]].building
                b.burn_stage = message[3]
                if message[3] > STAGES_BEFORE_BURN:
                    b.burn_stage = STAGES_BEFORE_BURN
            case MessageType.COLLAPSE_STAGE_INCREASE:
                # message is (posx, posy, collapse_stage)
                b = self.game.map.grid[message[1]][message[2]].building
                b.collapse_stage = message[3]
                if message[3] > STAGES_BEFORE_COLLAPSE:
                    b.collapse_stage = STAGES_BEFORE_COLLAPSE
            case MessageType.WALKER_SPAWN:
                b = self.game.map.grid[message[1]][message[2]].building
                t = walker_type(message[4], to_num=False)
                if t == Engineer:
                    b.engineer_do(self.game.map)
                    self.game.walkers.append(b.engineer)
                elif t == Farm_Boy:
                    b.deliver(self.game.map)
                    self.game.walkers.append(b.farm_boy)
                elif t == Market_Buyer:
                    b.fill(self.game.map)
                    self.game.walkers.append(b.buyer)
                elif t == Market_Trader:
                    b.trade(self.game.map)
                    self.game.walkers.append(b.trader)
                elif t == Migrant:
                    b.migrate(self.game.map, force=True)
                    self.game.walkers.append(b.migrant)
                elif t == Prefect:
                    b.prefect_do(self.game.map)
                    self.game.walkers.append(b.prefect)
                elif t == Tax_Collector:
                    b.collect(self.game.map)
                    self.game.walkers.append(b.tax_collector)
            case MessageType.GRANARY_STOCK:
                # farm boy
                fb = self.game.map.grid[message[1]][message[2]].building.farm_boy
                fb.granary.stock()
                fb.destination = (fb.spawn_road.tile.posx, fb.spawn_road.tile.posy)
                fb.state = Farm_Boy_State.TO_FARM
            case MessageType.GRANARY_UNSTOCK:
                # market buyer
                mb = self.game.map.grid[message[1]][message[2]].building.buyer
                mb.granary.unstock()
                mb.destination = (mb.spawn_road.tile.posx, mb.spawn_road.tile.posy)
                mb.state = Market_Buyer_State.TO_MARKET
            case MessageType.COLLAPSE_STAGE_RESET:
                self.game.map.grid[message[1]][message[2]].building.collapse_stage = 0
            case MessageType.BURN_STAGE_RESET:
                self.game.map.grid[message[1]][message[2]].building.burn_stage = 0
            case MessageType.MARKET_STOCK:
                # market buyer
                mb = self.game.map.grid[message[1]][message[2]].building.buyer
                mb.market.stock()
                if mb.granary.road_connection is None:
                    mb.destination = (mb.granary.tile.posx, mb.granary.tile.posy)
                else:
                    mb.destination = (mb.granary.road_connection.tile.posx,
                                      mb.granary.road_connection.tile.posy)
                mb.state = Market_Buyer_State.TO_GRANARY
            case MessageType.MARKET_SELL:
                # market trader
                mt = self.game.map.grid[message[1]][message[2]].building.trader
                mt.market.sell(message[3])
            case MessageType.WALKER_DESTROY:
                b = self.game.map.grid[message[1]][message[2]].building
                w = None
                t = walker_type(message[4], to_num=False)
                if t == Engineer: w = b.engineer
                elif t == Farm_Boy: w = b.farm_boy
                elif t == Market_Buyer: w = b.buyer
                elif t == Market_Trader: w = b.trader
                elif t == Migrant: w = b.migrant
                elif t == Prefect: w = b.prefect
                elif t == Tax_Collector: w = b.tax_collector
                self.game.remove_from_walkers(w)
            case MessageType.HOUSE_FOOD_STOCK:
                self.game.map.grid[message[1]][message[2]].food += message[3]
            case MessageType.HOUSE_EAT:
                self.game.map.grid[message[1]][message[2]].food -= message[3]
            case MessageType.SPEND_MONEY:
                self.game.denarii -= message[3]
            case MessageType.COLLECT_MONEY:
                self.game.denarii += message[3]

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

    def checkDaemon(self):
        # Check if c_daemon is already running
        process = subprocess.Popen(['pgrep', 'c_daemon'], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        if output:
            # c_daemon is already running
            print("c_daemon is already running")
        else:
            # c_daemon is not running, start it
            print("Starting c_daemon")
            # print([os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'c_daemon', 'bin', 'c_daemon'))])
            subprocess.Popen([os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'c_daemon', 'bin', 'c_daemon'))])

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
                        # print("Left button pressed at (x, y) = ", event.pos)

                        print("self.building est a : ", self.building)
                        # ------------------------------------------------------------------------------------Faire en clique droit
                    elif event.button == pg.BUTTON_RIGHT:
                        # print("Right button pressed at (x, y) = ", event.pos)
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
                        # print("Left button released at (x, y) = ", event.pos)
                    elif event.button == pg.BUTTON_RIGHT:
                        # print("Right button released at (x, y) = ", event.pos)
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
                            # print("into not(self.building)")
                            for button in self.list_button:
                                if button.listener_rect(mouse_pos):
                                    # print("button clicked")
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
