from Model.Tile import Tile, Tile_Type
from Model.Road import Road
from Model.House import House
from Model.New_House import New_House
from Model.Well import Well
from Model.Fountain import Fountain
from Model.Building import Building
from math import sqrt

MAP_DIM = 30


class Map:

    def __init__(self):
        self.grid = [[Tile(r, c, Tile_Type.Field) for c in range(MAP_DIM)] for r in range(MAP_DIM)]
        self.sizex = MAP_DIM
        self.sizey = MAP_DIM
        self.entry_point = None
        self.exit_point = None

    def __str__(self):
        string = ""
        for row in self.grid:
            for tile in row:
                string += str(tile) + " " * (13 - len(str(tile)))
            string += "\n"
        return string

    def take_all_ownership(self, player):
        for l in self.grid:
            for c in l:
                l.owner = player

    def build(self, posx, posy, type):
        b = type(self.grid[posx][posy])
        startx = int(posx - b.sizex / 2) + 1 if posx - b.sizex / 2 > 0 else 0
        endx = int(posx + b.sizex / 2) + 1
        for x in range(startx, endx):
            starty = int(posy - b.sizey / 2) + 1 if posy - b.sizey / 2 > 0 else 0
            endy = int(posy + b.sizey / 2) + 1
            for y in range(starty, endy):
                self.grid[x][y].build(b)
        return

    def destroy(self, posx, posy):
        b = self.grid[posx][posy].building
        startx = int(b.tile.posx - b.sizex / 2) + 1 if b.tile.posx - b.sizex / 2 > 0 else 0
        endx = int(b.tile.posx + b.sizex / 2) + 1
        for x in range(startx, endx):
            starty = int(b.tile.posy - b.sizey / 2) + 1 if b.tile.posy - b.sizey / 2 > 0 else 0
            endy = int(b.tile.posy + b.sizey / 2) + 1
            for y in range(starty, endy):
                self.grid[x][y].destroy()
        return

    def dist(self, x1, y1, x2, y2):
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # TO TEST
    def find_closest(self, posx, posy, type):
        closest_building = None
        closest_dist = MAP_DIM ** 2
        for x in range(MAP_DIM):
            for y in range(MAP_DIM):
                if self.is_type(x, y, type):
                    b = self.grid[x][y].building
                    if b.road_connection is not None and \
                        self.dist(posx, posy,
                                  b.road_connection.tile.posx,
                                  b.road_connection.tile.posy) < closest_dist:
                        closest_building = b
                        closest_dist = self.dist(posx, posy,
                                                 b.road_connection.tile.posx,
                                                 b.road_connection.tile.posy)
        return closest_building

    def is_type(self, posx, posy, t):
        if posx < 0 or posx >= self.sizex or posy < 0 or posy >= self.sizey:
            return False
        if t is None:
            return self.grid[posx][posy].building is None
        else:
            return type(self.grid[posx][posy].building) == t

    def road_connection(self, b):
        # Houses can be 1 tile away from the road
        d = 1 if isinstance(b, House) or isinstance(b, New_House) else 0
        x1 = int(b.tile.posx - d - b.sizex / 2)
        y1 = int(b.tile.posy - d - b.sizey / 2)
        x2 = int(b.tile.posx + d + b.sizex / 2) + 1
        y2 = int(b.tile.posy + d + b.sizey / 2) + 1
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if self.is_type(x, y, Road):
                    return self.grid[x][y].building
        return None

    def compute_water_coverage(self):
        for x in self.grid:
            for y in x:
                y.water_coverage = False
                # Use newly added attribute in Building but still keep the old one (just in case)
                if isinstance(y.building, Building):
                    y.building.water_coverage = False

        for x in range(MAP_DIM):
            for y in range(MAP_DIM):
                if self.is_type(x, y, Well):
                    for xx in range(x - 2 if x - 2 >= 0 else 0, x + 2 + 1 if x + 2 + 1
                                    < MAP_DIM else MAP_DIM):
                        for yy in range(y - 2 if y - 2 >= 0 else 0, y + 2 + 1 if y + 2 + 1
                                        < MAP_DIM else MAP_DIM):
                            # print(f"({xx}, {yy})")
                            self.grid[xx][yy].water_coverage = True
                            # Also usage of newly added Building attribute
                            if isinstance(self.grid[xx][yy].building, Building):
                                self.grid[xx][yy].building.water_coverage = True
                if self.is_type(x, y, Fountain):
                    for xx in range(x - 5 if x - 5 >= 0 else 0, x + 5 + 1 if x + 5 + 1 < MAP_DIM else MAP_DIM):
                        for yy in range(y - 5 if y - 5 >= 0 else 0, y + 5 + 1 if y + 5 + 1 < MAP_DIM else MAP_DIM):
                            # print(f"({xx}, {yy})")
                            self.grid[xx][yy].water_coverage = True
