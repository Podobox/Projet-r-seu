from Model.Building import Building


class Road(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)
        self.road_connection = self

    def __repr__(self):
        return "Road"
