from Model.Building import Building


class Senate(Building):

    def __init__(self, tile):
        super().__init__(5, 5, tile, job_offered=30)

    def __repr__(self):
        return "Senate"
