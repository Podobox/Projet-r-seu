from Model.Building import Building


class Fountain(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=4)

    def __repr__(self):
        return "Foutain"
