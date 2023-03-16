from enum import Enum
from Model.Player import Player

class Tile_Type(Enum):
    Water = 1
    Mountain = 2
    Field = 3
    Grass = 4


class Tile():

    def __init__(self, posx, posy, type):
        self.type = type
        self.building = None
        self.desirability = 0
        self.water_coverage = False
        self.posx = posx
        self.posy = posy
        self.player = None
    def __str__(self):
        ret = "("
        ret += str(self.building.__repr__()) if self.building is not None else str(self.type.name)
        ret += f", {self.desirability}, {self.water_coverage})"
        return ret

    def build(self, b):
        self.building = b

    def destroy(self):
        self.building = None
