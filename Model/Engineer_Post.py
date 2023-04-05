from Model.Building import Building
from Model.Engineer import Engineer
from Controller.Communication import walker_type


class Engineer_Post(Building):

    def __init__(self, tile):
        # size 1
        super().__init__(1, 1, tile, job_offered=6)
        self.engineer = None

    def __repr__(self):
        return "Engineer_Post"

    def engineer_do(self, map):
        if self.engineer is None:
            if self.is_active():
                self.engineer = Engineer(self, self.road_connection, map)
                self.communication.walker_spawn(self.tile.posx, self.tile.posy,
                                                walker_type(Engineer))
                return True
        else:
            if not self.is_active():
                self.engineer = None
            return False

