from Model.Building import Building
from Model.Farm_Boy import Farm_Boy


class Farm(Building):

    # production_speed is in cartloads / year
    def __init__(self, tile, production_speed):
        super().__init__(3, 3, tile, job_offered=10)
        self.production_speed = production_speed / 365 / 24 / 60  # cartloads / minutes
        self.production = 0
        self.last_production = None
        self.ready_to_collect = False
        self.farm_boy = None

    def __repr__(self):
        return "Wheat Farm"

    def __str__(self):
        string = super().__str__()
        string += f"\n\tProduction: {self.production}"
        return string

    def farm(self, date):
        if self.offer_jobs():
            return

        if self.production >= 1:
            self.ready_to_collect = True
            return

        if self.last_production is None:
            self.last_production = date
            return

        self.production += (date - self.last_production).seconds / 60 * self.production_speed
        self.last_production = date

    def collect(self):
        self.ready_to_collect = False
        self.production = 0
        print("collecting in farm")
        return True

    # return true if a farm boy was created
    def deliver(self, map):
        if self.farm_boy is None:
            if self.is_active():
                self.farm_boy = Farm_Boy(map, self.road_connection, self)
                return True
        else:
            if not self.is_active():
                self.farm_boy = None
            return False
