from Model.Building import Building
from Model.Migrant import Migrant
from random import random


class New_House(Building):
    def __init__(self, tile, sizex=1, sizey=1):
        super().__init__(sizex, sizey, tile, 0)
        self.migrant = None

    def __repr__(self):
        return "New_House"

    def migrate(self, map, force=False):
        if self.migrant is None:
            if self.road_connection is not None:
                # un peu de random sinon tous les migrants se supperposent c'est pas joli
                if force or random() < 0.005:
                    self.migrant = Migrant(map, map.entry_point, self)
                    return True
                else:
                    return False
        else:
            return False
