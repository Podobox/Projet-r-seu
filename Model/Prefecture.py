from Model.Building import Building
from Model.Prefect import Prefect
import Controller.Communication as com


class Prefecture(Building):

    def __init__(self, tile):
        # size 1
        super().__init__(1, 1, tile, job_offered=6)
        self.prefect = None

    def __repr__(self):
        return "Prefecture"

    def prefect_do(self, map):
        if self.prefect is None:
            if self.is_active():
                self.prefect = Prefect(self, self.road_connection, map)
                return True
        else:
            if not self.is_active():
                self.prefect = None
            return False

