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
<<<<<<< HEAD
        self.owner = None
=======
        self.player = None
    # def set_player(self,player):
    #     self.player = player
>>>>>>> 6a97858449dc6e689e357a1998f2a8860491ddd7

    def __str__(self):
        ret = "("
        ret += str(self.building.__repr__()) if self.building is not None else str(self.type.name)
        ret += f", {self.owner.id}"
        ret += f", {self.desirability}, {self.water_coverage})"
        return ret

    def build(self, b):
        self.building = b

    def destroy(self):
        self.building = None
