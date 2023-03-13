from Model.Building import Building


class Well(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=1)

    def __repr__(self):
        return "Well"
