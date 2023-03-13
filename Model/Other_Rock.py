from random import randint

from Model.Building import Building

other_rock_size = {
    1: (1, 1 / 2),
    2: (1, 1 / 2),
    3: (31 / 32, 5 / 24),
    4: (31 / 32, 10 / 24),
    5: (1, 3 / 16),
    6: (1, 1 / 32),
    7: (1, 1 / 32),
}


class Other_Rock(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)
        # self.type = randint(1, 28)
        self.type = randint(1, 7)
        self.compenX, self.compenY = other_rock_size[self.type]

    def __repr__(self):
        return "Other_Rock"
