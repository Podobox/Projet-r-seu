from Model.Destination_Walkers import Destination_Walkers
from Model.Walkers import Action
from Model.Granary import Granary
from enum import Enum


class Farm_Boy_State(Enum):
    WAITING_FARM = 1
    TO_GRANARY = 2
    TO_FARM = 3


class Farm_Boy(Destination_Walkers):

    def __init__(self, map, spawn_road, farm):
        super().__init__(map, spawn_road)
        self.farm = farm
        self.state = Farm_Boy_State.WAITING_FARM
        self.granary = None

    def __repr__(self):
        return "Farm_Boy"

    def find_destination(self):
        if self.state == Farm_Boy_State.WAITING_FARM:
            if self.farm.ready_to_collect:
                self.granary = self.map.find_closest(int(self.posx), int(self.posy), Granary)
                if self.granary is not None:
                    if self.granary.road_connection is None:
                        self.destination = (self.granary.tile.posx, self.granary.tile.posy)
                    else:
                        self.destination = (self.granary.road_connection.tile.posx,
                                            self.granary.road_connection.tile.posy)
                    self.farm.collect()
                    self.state = Farm_Boy_State.TO_GRANARY
        elif self.state == Farm_Boy_State.TO_GRANARY:
            if self.granary == \
                    self.map.grid[self.granary.tile.posx][self.granary.tile.posy].building:
                if self.granary.stock():
                    self.destination = (self.spawn_road.tile.posx, self.spawn_road.tile.posy)
                    self.state = Farm_Boy_State.TO_FARM
        else:  # TO_FARM
            self.state = Farm_Boy_State.WAITING_FARM

    def action_post(self):
        return Action.NONE
