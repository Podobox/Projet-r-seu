from random import randint

from Model.Building import Building

tree_size = {
    31: (31 / 32, 0),
    32: (31 / 32, 3 / 9),
    33: (31 / 32, 3 / 9),
    34: (31 / 32, 1 / 5),
    35: (31 / 32, 3 / 9),
    36: (31 / 32, 3 / 9)
}


class Tree(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)
        self.type = randint(31, 36)
        #self.type = 33
        self.compenX, self.compenY = tree_size[self.type]

    def __repr__(self):
        return "Tree"
