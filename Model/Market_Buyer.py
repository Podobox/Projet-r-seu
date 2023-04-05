from Model.Destination_Walkers import Destination_Walkers
from Model.Walkers import Action
from Model.Granary import Granary
from enum import Enum


class Market_Buyer_State(Enum):
    TO_GRANARY = 1
    TO_MARKET = 2


class Market_Buyer(Destination_Walkers):

    def __init__(self, map, spawn_road, market):
        super().__init__(map, spawn_road)
        self.market = market
        self.state = Market_Buyer_State.TO_MARKET
        self.granary = None
        self.building = market

    def __repr__(self):
        return "Market_Buyer"

    def find_destination(self, action):
        if self.state == Market_Buyer_State.TO_GRANARY:
            if action and self.granary == \
                    self.map.grid[self.granary.tile.posx][self.granary.tile.posy].building:
                if self.granary.unstock():
                    self.granary.communication.granary_unstock(self.market.tile.posx,
                                                               self.market.tile.posy)
                    self.destination = (self.spawn_road.tile.posx, self.spawn_road.tile.posy)
                    self.state = Market_Buyer_State.TO_MARKET
        else:  # TO_MARKET
            if not self.market.stock_greater_than(self.market.capacity - 100):
                self.granary = self.map.find_closest(int(self.posx), int(self.posy), Granary)
                if self.granary is not None and action:
                    if self.granary.road_connection is None:
                        self.destination = (self.granary.tile.posx, self.granary.tile.posy)
                    else:
                        self.destination = (self.granary.road_connection.tile.posx,
                                            self.granary.road_connection.tile.posy)
                    # cartload can't be refused because we left only when there was place
                    self.market.stock()
                    self.market.communication.market_stock(self.market.tile.posx,
                                                           self.market.tile.posy)
                    self.state = Market_Buyer_State.TO_GRANARY

    def action_post(self):
        return Action.NONE
