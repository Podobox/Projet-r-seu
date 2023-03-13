from Model.Destination_Walkers import Destination_Walkers
from Model.Walkers import Action


class Migrant(Destination_Walkers):

    def __init__(self, map, spawn, dest_house, leaving=False):
        super().__init__(map, spawn)
        self.destination = (dest_house.tile.posx, dest_house.tile.posy)
        self.house = self.map.grid[self.destination[0]][self.destination[1]].building
        self.leaving = leaving

    def __repr__(self):
        return "Migrant"

    def __str__(self):
        string = super().__str__()
        string += f"\n\tSpawn: {self.spawn_road}"
        return string

    def find_destination(self):
        if not self.leaving and self.house.tile.building is not self.house:
            self.destination = (self.map.exit_point.tile.posx,
                                self.map.exit_point.tile.posy)
            self.house = self.map.grid[self.destination[0]][self.destination[1]].building
            return False
        else:
            return True

    def action_post(self):
        if not self.leaving:
            if self.house.tile.building is self.house:
                return Action.BUILD_HOUSE
            else:
                return Action.NONE
        else:
            return Action.DESTROY_SELF
