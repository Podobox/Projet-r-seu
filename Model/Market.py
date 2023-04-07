from Model.Building import Building
from Model.Market_Buyer import Market_Buyer
from Model.Market_Trader import Market_Trader
from Controller.Communication import walker_type


class Market(Building):

    def __init__(self, tile):
        super().__init__(2, 2, tile, job_offered=5)
        self.capacity = 800
        self.current_stock = 0
        self.buyer = None
        self.trader = None

    def __repr__(self):
        return "Market"

    def stock_greater_than(self, n):
        return self.current_stock > n

    # return True if a cartload was stocked, else False
    def stock(self):
        if self.is_active() and not self.stock_greater_than(self.capacity - 100):
            self.current_stock += 100  # a cartload is broken down in 100 units
            return True
        else:
            return False

    # return the number of food sold
    def sell(self, n):
        if self.is_active():
            if self.stock_greater_than(n):
                self.current_stock -= n
                return n
            else:
                ret = self.current_stock
                self.current_stock = 0
                return ret
        else:
            return 0

    def fill(self, map):
        if self.buyer is None:
            if self.is_active():
                self.buyer = Market_Buyer(map, self.road_connection, self)
                self.communication.walker_spawn(self.tile.posx, self.tile.posy,
                                                walker_type(Market_Buyer))
                return True
        else:
            if not self.is_active():
                self.buyer = None
            return False

    def trade(self, map):
        if self.trader is None:
            if self.is_active():
                self.trader = Market_Trader(self, self.road_connection, map)
                self.communication.walker_spawn(self.tile.posx, self.tile.posy,
                                                walker_type(Market_Trader))
                return True
        else:
            if not self.is_active():
                self.trader = None
            return False
