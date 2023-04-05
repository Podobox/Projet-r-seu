from Model.Building import Building
from Model.Tax_Collector import Tax_Collector
from Controller.Communication import walker_type


class Forum(Building):

    def __init__(self, tile):
        super().__init__(2, 2, tile, job_offered=6)
        self.tax_collector = None

    def __repr__(self):
        return "Forum"

    def collect(self, map):
        if self.tax_collector is None:
            if self.is_active():
                self.tax_collector = Tax_Collector(self, self.road_connection, map)
                self.communication.walker_spawn(self.tile.posx, self.tile.posy,
                                                walker_type(Tax_Collector))
                return True
        else:
            if not self.is_active():
                self.tax_collector = None
            return False
