from Model.Building import Building
from Model.Tax_Collector import Tax_Collector
import Controller.Communication as com


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
                return True
        else:
            if not self.is_active():
                self.tax_collector = None
            return False
