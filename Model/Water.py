from random import randint

from Model.Building import Building


class Water(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)
        self.type = randint(120,127)

    def __repr__(self):
        return "Water"
