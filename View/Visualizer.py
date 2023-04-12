from operator import imod
from turtle import window_width
import pygame as pg
import tkinter as tk
import pygame

from Controller.barre_jeu import Barre
from Model.Engineer_Post import Engineer_Post
from Model.Granary import Granary
from Model.House import House
from Model.Map import Map, MAP_DIM
from Model.Other_Rock import Other_Rock
from Model.Rock import Rock
from Model.Tile import Tile_Type
from Model.Farm_Boy import Farm_Boy, Farm_Boy_State
from Model.Walkers import Direction
from Model.Sign import Sign, Sign_Type
from Model.Migrant import Migrant
from Model.Market_Buyer import Market_Buyer, Market_Buyer_State
from Model.Engineer import Engineer
from Model.Prefect import Prefect, Prefect_State
from Model.Market_Trader import Market_Trader
from Model.Tax_Collector import Tax_Collector
from Model.New_House import New_House
import Images as img
import sys
import os
from Model.Prefecture import Prefecture
from Model.Road import Road
from Model.Collapsed import Collapsed
from Model.Wheat_Farm import Wheat_Farm
from Model.Market import Market
from Model.Well import Well
from Model.Senate import Senate
from Model.Garden import Garden
from Model.Forum import Forum
from Model.Fountain import Fountain
from random import randint
from PIL import Image
from Controller.Button import Button
from View.FileMenu import FileMenu
from View.SideMenu import Menu
from View.Minimap import Minimap
from View.Chat import Chat
import Controller.Communication as com
from Model.Tree import Tree
from Model.Water import Water
# from View.PlayersConnect import PLayerConnected

# Get full screen size
root = tk.Tk()
# WINDOW_WIDTH = root.winfo_screenwidth()
# WINDOW_HEIGHT = root.winfo_screenheight()
WINDOW_WIDTH = 1700
WINDOW_HEIGHT = 840


# Just colors
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DGREEN = (55, 125, 35)
BLACK = (0, 0, 0)

# Size of cell according to zoom
cellSizeDict = {60: 30, 70: 35, 80: 40, 90: 45,
                100: 50, 150: 75, 200: 100, 300: 150}
DEFAULT_ZOOM = 60


# Takes x and y cartesian coordinates and transform into isometrics ones
def cartToIso(point):
    isoX = point[0] - point[1]
    isoY = (point[0] + point[1]) / 2
    return [isoX, isoY]


class Visualizer:

    # None = no overlay, 'Damage' = collapse, 'Fire' = burn, 'Water', 'Desirability'
    overlayType = None
    showGrid = False
    deplacementX = 0
    deplacementY = 0
    tmpDeplacementX = 0
    tmpDeplacementY = 0
    GAME_WIDTH = WINDOW_WIDTH
    GAME_HEIGHT = WINDOW_HEIGHT
    zoom = DEFAULT_ZOOM
    MODE_FILE_MENU = False
    showPlayers = False
    buildingMode = False

    def __init__(self, list_button, game, backup, communication):
        # Create pg window
        self.game = game
        global WINDOW_HEIGHT, WINDOW_WIDTH
        self.window = pg.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pg.FULLSCREEN)
        WINDOW_WIDTH, WINDOW_HEIGHT = self.window.get_size()
        self.GAME_WIDTH = WINDOW_WIDTH
        self.GAME_HEIGHT = WINDOW_HEIGHT
        # self.imgavatar = PLayerConnected(self.window, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.menu = Menu(self.window, WINDOW_WIDTH, WINDOW_HEIGHT, self.game, self.isoToCart, self)
        self.menu_displayed = False
        self.list_button = list_button
        self.zoom = DEFAULT_ZOOM
        self.images = {zoom: dict() for zoom in cellSizeDict}
        self.barre = Barre(self.window, WINDOW_WIDTH, WINDOW_HEIGHT, False, self)
        # self.barre.barre_function()
        self.fileMenu = FileMenu(self.window, WINDOW_WIDTH, WINDOW_HEIGHT, backup, game)
        #self.images = dict()
        self.minimap = Minimap(self.window, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.chat = Chat(self.window, WINDOW_WIDTH, WINDOW_HEIGHT, communication)

        self.loadImages()
        return

    def loadImages(self):
        scriptDir = sys.path[0]
        for filename in os.listdir(os.path.join(scriptDir, "Images")):
            if filename.endswith("png"):
                f = os.path.join(scriptDir, "Images", filename)
                i = pg.image.load(f).convert_alpha()
                for zoom in cellSizeDict:
                    size = cellSizeDict[zoom]
                    self.images[zoom][filename] = pg.transform.scale(
                        i, (i.get_width() * zoom / DEFAULT_ZOOM, i.get_height() * zoom / DEFAULT_ZOOM))
    def is_owner(self,MAP, x, y):
        return MAP.grid[x][y].owner == com.ME
        
    def update(self, map, walkers):
        self.list_button = []
        # Edge of each cell of the grid is 20px in cartesian
        # self.zoom = 100
        cellSize = cellSizeDict[self.zoom]
        # Draw the tiles
        self.window.fill(BLACK)

        self.placeIsoTiles(cellSize,
                           [WINDOW_HEIGHT / 2 + WINDOW_WIDTH / 4 -
                               (cellSize * MAP_DIM) / 2, WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 4 - (cellSize * MAP_DIM) / 2],
                           map, walkers)

        # Then the grid
        if self.showGrid:
            self.drawIsometricGrid([WINDOW_HEIGHT / 2 + WINDOW_WIDTH / 4 - (cellSize * MAP_DIM) / 2,
                                    WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 4 - (cellSize * MAP_DIM) / 2],
                                   MAP_DIM, cellSize)

        # Draw the game menu
        self.menu_displayed = False
        if not(self.menu_displayed):
            tmp_buttons = self.menu.display()
            #self.list_button = self.list_button + tmp_buttons
            self.list_button = (set(self.list_button) | set(tmp_buttons))
            self.menu_displayed = True

        if self.buildingMode != False:
            # self.window.blit(self.buildingMode[0], self.buildingMode[1])
            self.displayBuildingMode(map)

        if self.MODE_FILE_MENU:
            self.list_button = (set(self.list_button) | set(self.fileMenu.display()))

        self.minimap.display(map, self.deplacementX + self.tmpDeplacementX,
                             self.deplacementY + self.tmpDeplacementY)

        self.chat.display(self.chat)
        # self.imgavatar.display()
        


        # Draw game barre
        self.barre.barre_function(self.game.denarii, self.game.population, self.game.date)
        self.list_button = (set(self.list_button) | set([self.barre.fileButton]))

        # if self.showPlayers:
        #     self.imgavatar.show_players_connected(self.window)
        #     self.showPlayers= False
        #     pygame.display.update()
        
        return self.list_button

    def update_walker(self, w, cellSize, tileDIM, origin):
        # cellSize = cellSizeDict[self.zoom]
        # tileDIM = cellSize
        # origin = [WINDOW_HEIGHT / 2 + WINDOW_WIDTH / 4 - (cellSize * MAP_DIM)
                  # / 2, WINDOW_HEIGHT / 2 - WINDOW_WIDTH / 4 - (cellSize * MAP_DIM) / 2]
        imgCode = ""
        offsetx = 0
        offsety = 0
        match w.direction:
            case Direction.UP:
                imgCode = "ne"
                offsetx = 1
            case Direction.DOWN:
                imgCode = "so"
                offsetx = -1
            case Direction.LEFT:
                imgCode = "no"
                offsety = 1
            case Direction.RIGHT:
                imgCode = "se"
                offsety = -1
            case None:
                imgCode = "s"
                offsety = -0.7
                offsetx = -0.7
        imgCodeNum = w.roll_action()

        match w:
            case Farm_Boy():
                imgName = 'Cart_Pusher'
                compenX = cellSize
                compenY = cellSize / 4
                cimgName = ''
                if w.state == Farm_Boy_State.TO_GRANARY:
                    cimgName = 'Cart_Full'
                else:
                    cimgName = 'Cart_Empty'
                cart_posx = w.posx - 0.88 - 0.5 * offsetx
                cart_posy = w.posy - 0.5 - 0.5 * offsety
                if imgCode in ("so", "se"):
                    self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                      tileDIM, origin, imgName, imgCode + imgCodeNum,
                                      compenX, compenY)
                    self.displayImage(cart_posy, cart_posx, tileDIM, origin,
                                      cimgName, imgCode, compenX, compenY)
                else:
                    self.displayImage(cart_posy, cart_posx, tileDIM, origin,
                                      cimgName, imgCode, compenX, compenY)
                    self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                      tileDIM, origin, imgName, imgCode + imgCodeNum,
                                      compenX, compenY)
            case Engineer():
                imgName = 'Engineer'
                compenX = cellSize
                compenY = cellSize / 4
                self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                  tileDIM, origin, imgName, imgCode + imgCodeNum,
                                  compenX, compenY)
            case Market_Trader():
                imgName = 'Market_Trader'
                compenX = cellSize
                compenY = cellSize / 4
                self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                  tileDIM, origin, imgName, imgCode + imgCodeNum,
                                  compenX, compenY)
            case Tax_Collector():
                imgName = 'Tax_Collector'
                compenX = cellSize
                compenY = cellSize / 4
                self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                  tileDIM, origin, imgName, imgCode + imgCodeNum,
                                  compenX, compenY)
            case Prefect():
                imgName = ''
                match w.prefect_state:
                    case Prefect_State.ROAMING:
                        imgName = 'Prefect'
                    case Prefect_State.RETURN:
                        imgName = 'Prefect'
                    case Prefect_State.GOING_TO_FIRE:
                        imgName = 'Prefect_Bucket'
                    case Prefect_State.PUTING_OUT:
                        imgName = 'Prefect_Puting_Out'
                        imgCodeNum = int(imgCodeNum)
                        imgCodeNum %= 6  # only 6 images for puting out
                        imgCodeNum += 1
                        if imgCodeNum >= 10:
                            imgCodeNum = str(imgCodeNum)
                        else:
                            imgCodeNum = "0" + str(imgCodeNum)
                compenX = cellSize
                compenY = cellSize / 4
                self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                  tileDIM, origin, imgName, imgCode + imgCodeNum,
                                  compenX, compenY)
            case Market_Buyer():
                imgName = 'Market_Trader'
                compenX = cellSize
                compenY = cellSize / 4
                self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                  tileDIM, origin, imgName, imgCode + imgCodeNum,
                                  compenX, compenY)

            case Migrant():
                imgName = 'Boy'
                compenX = cellSize
                compenY = cellSize / 4
                cimgName = 'Cart_Migrant'
                cart_posx = w.posx - 0.85 + 0.5 * offsetx
                cart_posy = w.posy - 0.5 + 0.5 * offsety
                if imgCode in ("no", "ne"):
                    self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                      tileDIM, origin, imgName, imgCode + imgCodeNum,
                                      compenX, compenY)
                    self.displayImage(cart_posy, cart_posx, tileDIM, origin,
                                      cimgName, imgCode, compenX, compenY)
                else:
                    self.displayImage(cart_posy, cart_posx, tileDIM, origin,
                                      cimgName, imgCode, compenX, compenY)
                    self.displayImage(w.posy - 0.5, w.posx - 0.85,
                                      tileDIM, origin, imgName, imgCode + imgCodeNum,
                                      compenX, compenY)

    def displayImage(self, mapRow, mapCol, tileDIM, origin, imgName, imgCode, compensateX, compensateY, transparency=-1):
        originX = origin[0]
        originY = origin[1]

        # 3 lines below are the old, unoptimized way, keep it just in case
        # scriptDir = sys.path[0]
        # imagePath = os.path.join(scriptDir, "Images", imgName + '_' + imgCode + '.png')
        # displayImg = pg.image.load(imagePath)
        imagePath = imgName + '_' + imgCode + '.png'
        if transparency != -1:
            displayImg = self.images[self.zoom][imagePath].copy()
            displayImg.set_alpha(transparency)
        else:
            displayImg = self.images[self.zoom][imagePath]

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!! Ne surtout pas utiliser pg.transform dans la boucle principale !!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # c'est très lent et ca ralenti énormément le jeu, zoomé c'était plus jouable
        # il faut charger les images dans loadImages au lancement du jeu
        # imgSize = (displayImg.get_width() * self.zoom / DEFAULT_ZOOM,
                   # displayImg.get_height() * self.zoom / DEFAULT_ZOOM)
        # displayImg = pg.transform.scale(displayImg, imgSize)

        # if displayImg.get_height() != compensateY:
            # compensateY = displayImg.get_height()
        # if displayImg.get_width() != compensateX:
            # compensateX = displayImg.get_width()
        coordinates = cartToIso([originX + (tileDIM * mapRow), originY + (tileDIM * mapCol)])
        coordinates[0] -= compensateX
        coordinates[1] -= compensateY
        coordinates[0] += self.deplacementX + self.tmpDeplacementX
        coordinates[1] += self.deplacementY + self.tmpDeplacementY
        self.window.blit(displayImg, (coordinates[0], coordinates[1]))
        # displayImg.set_alpha(0)

    def isoToCart(self, point):
        x = point[0]
        y = point[1]
        point = [x, y]
        point[0] -= self.deplacementX
        point[1] -= self.deplacementY
        cartX = (point[0] + (2 * point[1])) / 2
        cartY = ((2 * point[1]) - point[0]) / 2
        cellSize = cellSizeDict[self.zoom]
        cartX -= self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2
        cartY -= self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2
        cartX /= cellSize
        cartY /= cellSize
        return [int(cartX), int(cartY)]

    def cartToIso(self, point):  # [0,0]
        cellSize = cellSizeDict[self.zoom]
        x = point[0]
        y = point[1]
        y *= cellSize
        x *= cellSize
        x += self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2
        y += self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2
        point = [x, y]
        cartY = ((2 * point[0]) + (2 * point[1])) / 4
        cartX = (2 * cartY) - (2 * point[1])
        cartX += self.deplacementX
        cartY += self.deplacementY
        return [int(cartX), int(cartY)]

    # Display the tiles(cells) of the map
    # self is the display, cellSize is length of each cell, origin is 2D coordinates of the origin,
    # Map is the table of value of each cell
    def placeIsoTiles(self, cellSize, origin, MAP, walkers):
        tileDIM = cellSize
        originX, originY = origin[0], origin[1]
        for sumRC in range(MAP_DIM * 2 - 1):
            for row in range(max(0, sumRC - 19), min(MAP_DIM, sumRC + 1)):
                column = sumRC - row
                # print(row, column)

        # first pass for where the walkers may walk so carts behind some of them don't
        # overlap
        for row in range(MAP_DIM):
            for column in range(MAP_DIM):
                if MAP.is_type(column, row, Road):
                    if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP, row, column,tileDIM, origin) 
                    else:
                        roadType = 0
                        roadType += 1 if (column >
                                        0 and MAP.is_type(column - 1, row, Road)) else 0
                        roadType += 2 if (row > 0 and MAP.is_type(column, row - 1, Road)) else 0
                        roadType += 4 if (column <
                                        MAP_DIM and MAP.is_type(column + 1, row, Road)) else 0
                        roadType += 8 if (row <
                                        MAP_DIM and MAP.is_type(column, row + 1, Road)) else 0
                        if roadType == 0:
                            roadType = 5
                        imgCode = '000' + (f'0{roadType}' if roadType < 10 else f'{roadType}')
                        imgName = 'Road'
                        compenX = cellSize
                        compenY = 0
                        self.displayImage(row, column, tileDIM, origin,
                                        imgName, imgCode, compenX, compenY)
                elif MAP.is_type(column, row, None):
                    if self.overlayType == 'Desirability':
                        desirabilityLevel = MAP.grid[column][row].desirability
                        self.showDesirabilityLevel(
                            row, column, tileDIM, origin, desirabilityLevel)
                    else:
                        match MAP.grid[column][row].type:
                            case Tile_Type.Water: pass
                            case Tile_Type.Mountain: pass
                            case Tile_Type.Field:
                                imgName = 'Field'
                                imgCode = '00001'
                                compenX = cellSize
                                compenY = cellSize * 1 / 12
                                self.displayImage(row, column, tileDIM, origin,
                                                  imgName, imgCode, compenX, compenY)
                            case Tile_Type.Grass:
                                imgName = 'Grass'
                                imgCode = '00010'
                                compenX = cellSize
                                compenY = 0
                                self.displayImage(row, column, tileDIM, origin,
                                                  imgName, imgCode, compenX, compenY)

        walker_iterator = iter(walkers)
        w = next(walker_iterator, None)
        for sumRC in range(MAP_DIM * 2 - 1):
            for row in range(max(0, sumRC - (MAP_DIM - 1)),
                             min(MAP_DIM, sumRC + 1)):
                column = sumRC - row
                # We display differently for each value of map cell
                match MAP.grid[column][row].building:
                    case 0:  # test value
                        tilePoints = [
                            cartToIso([originX + (tileDIM * row),
                                      originY + (tileDIM * column)]),
                            cartToIso([originX + (tileDIM * (row + 1)),
                                      originY + (tileDIM * column)]),
                            cartToIso([originX + (tileDIM * (row + 1)),
                                      originY + (tileDIM * (column + 1))]),
                            cartToIso([originX + (tileDIM * row),
                                      originY + (tileDIM * (column + 1))])
                        ]
                        # pg.draw.polygon(self.window, GREEN, tilePoints, )
                    case House():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                
                        else:
                            houseNames = {
                                1: 'SmallTent', 2: 'LargeTent', 3: 'SmallShack', 4: 'LargeShack'}
                            imgName = houseNames[MAP.grid[column][row].building.level.value]
                            imgCode = '00001'
                            compenVal = {1: [cellSize * 31 / 32, 0],
                                         2: [cellSize * 31 / 32, cellSize / 8],
                                         3: [cellSize * 31 / 32, 0],
                                         4: [cellSize * 31 / 32, cellSize * 3 / 32]}
                            compenX, compenY = compenVal[MAP.grid[column]
                                                         [row].building.level.value]
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case New_House():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                
                        else:
                            imgName = 'NewHouse'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case Water():
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        else:
                            isSea = True
                            for dx in range(-1, 2, 1):
                                if not isSea:
                                    break
                                for dy in range(-1, 2, 1):
                                    if not isSea:
                                        break
                                    # col = x, row = y
                                    x = column + dx
                                    y = row + dy
                                    if x < 0 or y < 0 or x >= MAP_DIM or y >= MAP_DIM:
                                        continue
                                    if not isinstance(MAP.grid[x][y].building, Water):
                                        isSea = False
                                        break
                            if isSea:
                                imgName = 'Land1a'
                                imgCode = '00' + \
                                    str(MAP.grid[column][row].building.type)
                                compenX = cellSize
                                compenY = 0
                                self.displayImage(
                                    row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                            else:
                                posd = {3: [0, -1],
                                        2: [1, 0], 
                                        1: [0, 1], 
                                        0: [-1, 0]}
                                posMark = []
                                for i in range(len(posd)):
                                    dx, dy = posd[i]
                                    x = column + dx
                                    y = row + dy
                                    if x < 0 or y < 0 or x >= MAP_DIM or y >= MAP_DIM or \
                                            MAP.is_type(x, y, Water):
                                        posMark.append(i)
                                posMark.sort()
                                # print(column, row, posMark)
                                imgName = 'Land1a'
                                # Incomplete
                                match tuple(posMark):
                                    case ():
                                        imgCode = '00199'
                                    case (0, 1):
                                        imgCode = '00144'
                                    case (0, 1, 3):
                                        imgCode = '00130'
                                    case (0, 2, 3):
                                        imgCode = '00143'
                                    case (0, 3):
                                        imgCode = '00157'
                                    case (0, 1, 2, 3):
                                        imgCode = '00001'
                                        if not MAP.is_type(column + 1, row - 1, Water):
                                            imgCode = '00170'
                                    case _:
                                        imgCode = '00001'
                                compenX = cellSize
                                compenY = 0
                                self.displayImage(
                                    row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case Tree():
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        else:
                            imgName = 'Land1a'
                            compenX = cellSize * \
                                MAP.grid[column][row].building.compenX
                            compenY = cellSize * \
                                MAP.grid[column][row].building.compenY
                            imgCode = '000' + \
                                str(MAP.grid[column][row].building.type)
                            self.displayImage(
                                row, column, tileDIM, origin, imgName, imgCode, compenX, compenY)
                    case Rock():
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP, row, column,tileDIM, origin) 
                        else:
                            imgName = 'Land1a'
                            compenX = cellSize * \
                                MAP.grid[column][row].building.compenX
                            compenY = cellSize * \
                                MAP.grid[column][row].building.compenY
                            imgCode = '00' + \
                                str(MAP.grid[column][row].building.type)

                            self.displayImage(row, column, tileDIM, origin,
                                            imgName, imgCode, compenX, compenY)
                            imgCode = '00' + str(MAP.grid[column][row].building.type)
                            self.displayImage(row, column, tileDIM, origin,
                                            imgName, imgCode, compenX, compenY)
                    case Other_Rock():
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP, row, column,tileDIM, origin) 
                        else:
                            imgName = 'plateau'
                            compenX = cellSize * \
                                MAP.grid[column][row].building.compenX
                            compenY = cellSize * \
                                MAP.grid[column][row].building.compenY
                            imgCode = '0000' + \
                                str(MAP.grid[column][row].building.type)
                            self.displayImage(row, column, tileDIM, origin,
                                            imgName, imgCode, compenX, compenY)
                            imgCode = '0000' + str(MAP.grid[column][row].building.type)
                            self.displayImage(row, column, tileDIM, origin,
                                            imgName, imgCode, compenX, compenY)
                    case Prefecture():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        
                        else:
                            imgName = 'Prefecture'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            if MAP.grid[column][row].building.is_active():
                                imgName = 'PrefectureFlag'
                                code = randint(1, 10)
                                imgCode = f'000{code}' if code >= 10 else f'0000{code}'
                                compenX = cellSize * 3 / 8
                                compenY = cellSize * 5 / 8
                                self.displayImage(row, column, tileDIM, origin,
                                                  imgName, imgCode, compenX, compenY)
                    # case Road():
                        # roadType = 0
                        # roadType += 1 if (column
                                          # > 0 and MAP.is_type(column - 1, row, Road)) else 0
                        # roadType += 2 if (row > 0 and MAP.is_type(column, row - 1, Road)) else 0
                        # roadType += 4 if (column
                                          # < MAP_DIM and MAP.is_type(column + 1, row, Road)) else 0
                        # roadType += 8 if (row
                                          # < MAP_DIM and MAP.is_type(column, row + 1, Road)) else 0
                        # if roadType == 0:
                            # roadType = 5
                        # imgCode = '000' + (f'0{roadType}' if roadType < 10 else f'{roadType}')
                        # imgName = 'Road'
                        # compenX = cellSize
                        # compenY = 0
                        # self.displayImage(row, column, tileDIM, origin,
                                          # imgName, imgCode, compenX, compenY)
                    case Collapsed():
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        else:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                            imgName, imgCode, compenX, compenY)
                    case Engineer_Post():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,
                                row, column, tileDIM, origin,)
                        else:
                            imgName = 'EngineerPost'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize * 5 / 8
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            if MAP.grid[column][row].building.is_active():
                                imgName = 'EngineerPostFlag'
                                code = randint(1, 9)
                                imgCode = f'0000{code}'
                                compenX = cellSize * 5 / 8
                                compenY = cellSize * 7 / 8
                                self.displayImage(row, column, tileDIM, origin,
                                                  imgName, imgCode, compenX, compenY)
                    case Wheat_Farm():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        elif MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column:
                            imgName = 'Farm'
                            imgCode = '00001'
                            compenX = cellSize * 2
                            compenY = cellSize * 5 / 8
                            rowFarm = row - 1
                            columnFarm = column - 1
                            self.displayImage(rowFarm, columnFarm, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'WheatField'
                            prodLevel = min(
                                5, MAP.grid[column][row].building.production * 5)
                            prodLevel = max(1, prodLevel)
                            prodLevel = int(prodLevel)
                            imgCode = f'0000{prodLevel}'
                            compenX = 0
                            comYVal = {1: - cellSize / 2, 2: - cellSize * 3 / 8,
                                       3: - cellSize / 4, 4: 0, 5: cellSize / 4}
                            compenY = comYVal[prodLevel]
                            x = columnFarm + 1
                            y = rowFarm - 1
                            posWheatField = [[x + 1, y], [x - 1, y + 2], [x + 1, y + 1],
                                             [x, y + 2], [x + 1, y + 2]]
                            for [columnField, rowField] in posWheatField:
                                self.displayImage(rowField, columnField, tileDIM, origin,
                                                  imgName, imgCode, compenX, compenY)
                                pass
                    case Market():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        elif MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column:
                            # print(row, column)
                            imgName = 'Market'
                            imgCode = '00001'
                            compenX = cellSize * 2
                            compenY = cellSize / 8
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case Granary():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        elif MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column:
                            imgName = 'GranaryBase'
                            imgCode = '00001'
                            compenX = 0
                            compenY = cellSize / 2
                            rowBase = row - 2
                            columnBase = column + 1
                            self.displayImage(rowBase, columnBase, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Granary'
                            imgCode = '00001'
                            compenX = cellSize / 16
                            compenY = cellSize / 16
                            rowGranary = rowBase - 2
                            columnGranary = columnBase - 3
                            self.displayImage(rowGranary, columnGranary, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            stockLevel = int(
                                MAP.grid[column][row].building.current_stock / 3)
                            stockLevel = min(4, stockLevel)
                            posWindow = [[row - 2, column - 1],
                                         [row - 1, column - 2],
                                         [row - 2, column - 1],
                                         [row - 1, column - 1]]
                            compenVal = [[cellSize * 13 / 16, cellSize * 3 / 8],
                                         [cellSize / 16, cellSize * 7 / 16],
                                         [0, cellSize / 16],
                                         [cellSize / 16, cellSize * 9 / 16]]
                            # stockLevel = 4
                            for index in range(stockLevel):
                                [rowWindow, columnWindow] = posWindow[index]
                                imgName = 'GranaryWindow'
                                imgCode = f'0000{index + 1}'
                                [compenX, compenY] = compenVal[index]
                                self.displayImage(rowWindow, columnWindow, tileDIM, origin,
                                                  imgName, imgCode, compenX, compenY)
                    case Well():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        else:
                            imgName = 'Well'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize * 3 / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case Sign():
                        if self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        else:
                            imgName = 'Sign_'
                            if MAP.grid[column][row].building.type == Sign_Type.Enter:
                                imgName += 'Enter'
                            else:
                                imgName += 'Exit'
                            imgCode = 'se'
                            compenX = cellSize * 31 / 32
                            compenY = cellSize * 5 / 8
                            self.displayImage(row, column, tileDIM, origin,
                                            imgName, imgCode, compenX, compenY)
                    case None:
                        match MAP.grid[column][row].type:
                            case Tile_Type.Water:  
                                if self.overlayType == 'Tile':
                                    self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                                else:pass
                            case Tile_Type.Mountain:
                                if self.overlayType == 'Tile':
                                    self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                                else:pass
                            case Tile_Type.Field:
                                if self.overlayType == 'Tile':
                                    self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                                else:
                                    imgName = 'Field'
                                    imgCode = '00001'
                                    compenX = cellSize * 31 / 32
                                    compenY = cellSize / 16
                                    self.displayImage(row, column, tileDIM, origin,
                                                        imgName, imgCode, compenX, compenY)
                            case Tile_Type.Grass:
                                if self.overlayType == 'Tile':
                                    self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                                else:
                                    imgName = 'Grass'
                                    imgCode = '00010'
                                    compenX = cellSize
                                    compenY = 0
                                    self.displayImage(MAP,row, column, tileDIM, origin,
                                                    imgName, imgCode, compenX, compenY)
                    case Senate():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                                    self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        elif MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column:
                            imgName = 'Senate'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            rowBase = row - 5
                            columnBase = column - 1
                            self.displayImage(rowBase, columnBase, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case Garden():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP, row, column,tileDIM, origin) 
                        else:
                            imgName = 'Garden'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize / 16
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case Forum():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Water':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            covered = MAP.grid[column][row].building.water_coverage
                            self.showWaterCoverage(
                                row, column, tileDIM, origin, posType, covered)
                        elif self.overlayType == 'Desirability':
                            desirabilityLevel = MAP.grid[column][row].building.tile.desirability
                            self.showDesirabilityLevel(
                                row, column, tileDIM, origin, desirabilityLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        elif MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column:
                            imgName = 'Forum'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = cellSize * 9 / 32
                            rowBase = row - 2
                            columnBase = column - 1
                            self.displayImage(rowBase, columnBase, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    case Fountain():
                        if MAP.grid[column][row].building.burning:
                            imgName = 'Collapsed'
                            imgCode = '00001'
                            compenX = cellSize
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'Burning'
                            imgCode = f'0000{randint(1, 8)}'
                            compenX = cellSize / 2
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                        elif self.overlayType == 'Fire':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.burn_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Damage':
                            posType = 1
                            if MAP.grid[column][row].building == MAP.grid[column - 1][row].building:
                                posType += 1
                            if MAP.grid[column][row].building == MAP.grid[column][row - 1].building:
                                posType += 2
                            riskLevel = MAP.grid[column][row].building.collapse_stage
                            if not (MAP.grid[column][row].building.tile.posy == row and MAP.grid[column][row].building.tile.posx == column):
                                riskLevel = 0
                            self.showBurnCollapseRisk(
                                row, column, tileDIM, origin, posType, riskLevel)
                        elif self.overlayType == 'Tile':
                            self.showPlayerCase(MAP,row, column,tileDIM, origin) 
                        else:
                            imgName = 'Fountain'
                            imgCode = '00001'
                            compenX = cellSize * 31 / 32
                            compenY = 0
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                            imgName = 'FountainWater'
                            imgCode = f'0000{randint(1, 7)}'
                            compenX = cellSize * 9 / 16
                            compenY = cellSize / 4
                            self.displayImage(row, column, tileDIM, origin,
                                              imgName, imgCode, compenX, compenY)
                    # case None:
                        # if self.overlayType == 'Desirability':
                            # desirabilityLevel = MAP.grid[column][row].desirability
                            # self.showDesirabilityLevel(
                                # row, column, tileDIM, origin, desirabilityLevel)
                        # else:
                            # imgName = 'Grass'
                            # imgCode = '00010'
                            # compenX = cellSize
                            # compenY = 0
                            # self.displayImage(row, column, tileDIM, origin,
                                              # imgName, imgCode, compenX, compenY)

                while w and int(w.posx) <= column and int(w.posy) <= row:
                    # print("DISPLAYING", w)
                    self.update_walker(w, cellSize, tileDIM, origin)
                    w = next(walker_iterator, None)

    # Display the grid of the map
    # self: display, origin: 2D coordinates of origin, size: map's dimension
    # cellSize: edge's length of cell

    def drawIsometricGrid(self, origin, size, cellSize):
        hw = cellSize * size
        gridColor = BLUE
        borderPoints = [cartToIso(origin),
                        cartToIso([origin[0], origin[1] + hw]),
                        cartToIso([origin[0] + hw, origin[1] + hw]),
                        cartToIso([origin[0] + hw, origin[1]])]
        for bP in borderPoints:
            bP[0] += self.deplacementX + self.tmpDeplacementX - 1
            bP[1] += self.deplacementY + self.tmpDeplacementY - 1
        # Draw grid's border
        pg.draw.polygon(self.window, gridColor, borderPoints, 2)
        # Draw inner lines
        for colRow in range(1, size):
            dim = cellSize * colRow
            start_point = cartToIso([origin[0], origin[1] + dim])
            start_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            start_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            end_point = cartToIso([hw + origin[0], origin[1] + dim])
            end_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            end_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            pg.draw.line(self.window, gridColor, start_point, end_point, 1)
            start_point = cartToIso([origin[0] + dim, origin[1]])
            start_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            start_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            end_point = cartToIso([origin[0] + dim, origin[1] + hw])
            end_point[0] += self.deplacementX + self.tmpDeplacementX - 1
            end_point[1] += self.deplacementY + self.tmpDeplacementY - 1
            pg.draw.line(self.window, gridColor, start_point, end_point, 1)

    # FIXME unused

    def drawMenu(self):
        scriptDir = sys.path[0]
        imagePath = os.path.join(scriptDir + "/Images/play_menu/paneling_00017.png")
        pannelMenu = pg.image.load(imagePath)

        img = Image.open(imagePath)
        imgWidth = img.width
        imgHeight = img.height
        coefficient = WINDOW_HEIGHT / imgHeight

        pannelMenu = pg.transform.scale(pannelMenu, (imgWidth * coefficient, WINDOW_HEIGHT))
        self.window.blit(pannelMenu, (WINDOW_WIDTH - (imgWidth * coefficient), 0))
        return

    def changeBuildingMode(self, buttonclicked=-1, pos=-1, finalpos=-1):

        if buttonclicked == -1:
            self.buildingMode = False
            return

        correct_x = 0
        correct_y = 0

        if buttonclicked.building == Forum:
            correct_x = -2
            correct_y = -1
        elif buttonclicked.building == Senate:
            correct_x = -5
            correct_y = -1
        elif buttonclicked.building == Wheat_Farm:
            correct_x = -1
            correct_y = -1
        elif buttonclicked.building == Granary:
            correct_x = -2
            correct_y = 1

        if finalpos != -1:
            # faut rajouter dans buildingMode une position final puis on s'occupe du rest dans displayBuildingMode()
            obj = buttonclicked.obj
            pos = self.isoToCart(pos)
            finalpos = self.isoToCart(finalpos)
            self.buildingMode = [buttonclicked.building, obj,
                                 (pos[0] + correct_x, pos[1] + correct_y), finalpos]
            return

        obj = buttonclicked.obj
        pos = self.isoToCart(pos)
        # pos = self.cartToIso(pos)
        self.buildingMode = [buttonclicked.building, obj, (pos[0] + correct_x, pos[1] + correct_y)]
        return

    def displayBuildingMode(self, MAP):

        if len(self.buildingMode) == 4:
            init_pos = self.buildingMode[2]
            final_pos = self.buildingMode[3]

            if self.buildingMode[0] == Senate or self.buildingMode[0] == Wheat_Farm:
                row = self.buildingMode[2][0]
                column = self.buildingMode[2][1]
                cellSize = cellSizeDict[self.zoom]
                tileDIM = cellSize
                origin = [self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4 -
                          (cellSize * MAP_DIM) / 2, self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2]

                settings = self.getSettingsBuilding(cellSize, row, column, MAP)
                self.displayImage(row, column, tileDIM, origin,
                                  settings[0], settings[1], settings[2], settings[3], 128)
                return

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
                    row = mini_x
                    column = mini_y
                    cellSize = cellSizeDict[self.zoom]
                    tileDIM = cellSize
                    origin = [self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2,
                              self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2]
                    settings = self.getSettingsBuilding(cellSize, row, column, MAP)
                    self.displayImage(row, column, tileDIM, origin,
                                      settings[0], settings[1], settings[2], settings[3], 128)
                    if self.buildingMode[0] == Market or self.buildingMode[0] == Forum:
                        mini_x += 2
                    elif self.buildingMode[0] == Granary:
                        mini_x += 3
                    else:
                        mini_x += 1
                mini_x = old_mini_x
                if self.buildingMode[0] == Market or self.buildingMode[0] == Forum:
                    mini_y += 2
                elif self.buildingMode[0] == Granary:
                    mini_y += 3
                else:
                    mini_y += 1
            return

        row = self.buildingMode[2][0]
        column = self.buildingMode[2][1]
        cellSize = cellSizeDict[self.zoom]
        tileDIM = cellSize
        origin = [self.GAME_HEIGHT / 2 + self.GAME_WIDTH / 4
                  - (cellSize * MAP_DIM) / 2, self.GAME_HEIGHT / 2 - self.GAME_WIDTH / 4 - (cellSize * MAP_DIM) / 2]

        settings = self.getSettingsBuilding(cellSize, row, column, MAP)
        self.displayImage(row, column, tileDIM, origin,
                          settings[0], settings[1], settings[2], settings[3], 128)
        return

    def getSettingsBuilding(self, cellSize, row, column, MAP):

        if self.buildingMode[0] == Prefecture:
            imgName = 'Prefecture'
            imgCode = '00001'
            compenX = cellSize
            compenY = cellSize / 4
        elif self.buildingMode[0] == Road:
            roadType = 0
            roadType += 1 if (column > 0 and isinstance(MAP.grid[column - 1][row], Road)) else 0
            roadType += 2 if (row > 0 and isinstance(MAP.grid[column][row - 1], Road)) else 0
            roadType += 4 if (column < MAP_DIM
                              - 1 and isinstance(MAP.grid[column + 1][row], Road)) else 0
            roadType += 8 if (row < MAP_DIM
                              - 1 and isinstance(MAP.grid[column][row + 1], Road)) else 0
            if roadType == 0:
                roadType = 5
            imgCode = '000' + (f'0{roadType}' if roadType < 10 else f'{roadType}')
            imgName = 'Road'
            compenX = cellSize
            compenY = 0
        elif self.buildingMode[0] == Engineer_Post:
            imgName = 'EngineerPost'
            imgCode = '00001'
            compenX = cellSize
            compenY = cellSize * 3 / 4
        elif self.buildingMode[0] == New_House:
            imgName = 'SmallTent'
            imgCode = '00001'
            compenX = cellSize
            compenY = 0
        elif self.buildingMode[0] == "destroy":
            imgName = 'Grass'
            imgCode = '00010'
            compenX = cellSize
            compenY = 0
        elif self.buildingMode[0] == Market:
            imgName = 'Market'
            imgCode = '00001'
            compenX = cellSize * 2
            compenY = cellSize / 8
        elif self.buildingMode[0] == Wheat_Farm:
            imgName = 'Farm'
            imgCode = '00001'
            compenX = cellSize * 2
            compenY = cellSize * 5 / 8
        elif self.buildingMode[0] == Granary:
            imgName = 'GranaryBase'
            imgCode = '00001'
            compenX = 0
            compenY = cellSize / 2
        elif self.buildingMode[0] == Well:
            imgName = 'Well'
            imgCode = '00001'
            compenX = cellSize
            compenY = cellSize * 3 / 4
        elif self.buildingMode[0] == Fountain:
            imgName = 'Fountain'
            imgCode = '00001'
            compenX = cellSize * 31 / 32
            compenY = 0
        elif self.buildingMode[0] == Senate:
            imgName = 'Senate'
            imgCode = '00001'
            compenX = cellSize
            compenY = 0
        elif self.buildingMode[0] == Garden:
            imgName = 'Garden'
            imgCode = '00001'
            compenX = cellSize
            compenY = cellSize / 16
        elif self.buildingMode[0] == Forum:
            imgName = 'Forum'
            imgCode = '00001'
            compenX = cellSize
            compenY = cellSize * 9 / 32

        return [imgName, imgCode, compenX, compenY]

    def showBurnCollapseRisk(self, row, column, tileDIM, origin, posType, riskLevel):
        imgName = 'FireRiskField'
        imgCode = f'0000{posType}'
        compenX = tileDIM
        compenY = 0
        self.displayImage(row, column, tileDIM, origin,
                          imgName, imgCode, compenX, compenY)

        if riskLevel == 0:
            return
        imgCode = f'0000{int((riskLevel - 1) / 3 + 1)}'
        imgName = 'FireRiskPillarFoot'
        compenX = tileDIM * 5 / 8
        compenY = tileDIM * 1 / 4
        self.displayImage(row, column, tileDIM, origin,
                          imgName, imgCode, compenX, compenY)
        if riskLevel > 1:
            imgName = 'FireRiskPillar'
            compenX = tileDIM * 23 / 64
            compenY = - tileDIM * 1 / 8
            for i in range(riskLevel - 2):
                compenY += tileDIM / 4
                self.displayImage(row, column, tileDIM, origin,
                                  imgName, imgCode, compenX, compenY)
            imgName = 'FireRiskPillarTop'
            compenY += tileDIM
            compenX = tileDIM * 97 / 128
            self.displayImage(row, column, tileDIM, origin,
                              imgName, imgCode, compenX, compenY)

    def showWaterCoverage(self, row, column, tileDIM, origin, posType, covered):
        if not covered:
            self.showBurnCollapseRisk(row, column, tileDIM, origin, posType, 0)
        else:
            imgName = 'WaterOverlay'
            imgCode = f'0000{posType}'
            compenX = tileDIM
            compenY = 0
            self.displayImage(row, column, tileDIM, origin,
                              imgName, imgCode, compenX, compenY)
    def showPlayerCase(self,MAP, row, column, tileDIM, origin):
        if  self.is_owner( MAP,column, row):
            imgName = 'player_case'
            compenX = tileDIM
            compenY = 0
            imgCode =''
            self.displayImage(row, column, tileDIM, origin, imgName,imgCode, compenX, compenY)
        else:
            imgName = 'other_player_case'
            imgCode =''
            compenX = tileDIM
            compenY = 0
            self.displayImage(row, column, tileDIM, origin, imgName,imgCode, compenX, compenY)

    
    def showDesirabilityLevel(self, row, column, tileDim, origin, desirabilityLevel):
        desirabilityLevel = desirabilityLevel // 4
        if desirabilityLevel < -3:
            desirabilityLevel = -3
        elif desirabilityLevel > 7:
            desirabilityLevel = 7
        compenVal = {-3: [tileDim, 0],
                     -2: [tileDim, 0],
                     -1: [tileDim, 0],
                     1: [tileDim, 0],
                     2: [tileDim * 31 / 32, tileDim / 32],
                     3: [tileDim * 31 / 32, tileDim / 8],
                     4: [tileDim * 31 / 32, tileDim * 3 / 16],
                     5: [tileDim * 31 / 32, tileDim / 4],
                     6: [tileDim * 31 / 32, tileDim * 5 / 16],
                     7: [tileDim * 31 / 32, tileDim * 3 / 8]}
        if desirabilityLevel == 0:
            imgName = 'Grass'
            imgCode = '00010'
            compenX = tileDim
            compenY = 0
        else:
            imgName = 'SatisfactionPlateau'
            if desirabilityLevel < 0:
                imgCode = f'0000{desirabilityLevel + 4}'
            elif desirabilityLevel == 7:
                imgCode = '00010'
            else:
                imgCode = f'0000{desirabilityLevel + 3}'
            [compenX, compenY] = compenVal[desirabilityLevel]
        self.displayImage(row, column, tileDim, origin,
    
                          imgName, imgCode, compenX, compenY)
   





# Things left to render:
# Granary's Crane
# Newly created house (habitant not yet moved in)
# Build/Destroy preview
# Senate's flags
# Terrain (Grass, Trees, Rivers, Sea, Mountains, River banks)
# Workers if not finished
