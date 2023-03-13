from random import randint

from Model.Building import Building

rock_size = {
    290: (1, 2 / 12),
    291: (1, 1 / 5),
    292: (1, 1 / 4),
    293: (30 / 32, 3 / 12),
    294: (0, 0),
    295: (0, 0),
    296: (0, 0),
    297: (0, 0),
}


class Rock(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)
        self.type = randint(290, 293)
        # self.type = 292
        self.compenX, self.compenY = rock_size[self.type]

    def __repr__(self):
        return "Rock"
