from Model.Building import Building


class Garden(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)

    def __repr__(self):
        return "Garden"
