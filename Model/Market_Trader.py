from Model.Random_Walkers import Random_Walkers
from Model.House import House
from Model.Map import MAP_DIM


class Market_Trader(Random_Walkers):

    def __init__(self, market, spawn_road, map):
        super().__init__(35, 26, spawn_road, map)
        self.market = market
        self.building = market

    def __repr__(self):
        return "Market_Trader"

    def find_destination(self):
        self.destination = (self.market.road_connection.tile.posx,
                            self.market.road_connection.tile.posy)

    def action_while(self, date):
        wx = int(self.posx)
        wy = int(self.posy)

        d = 2
        bs = []
        for x in range(wx - d if wx - d > 0 else 0,
                       wx + d + 1 if wx + d < MAP_DIM else MAP_DIM):
            for y in range(wy - d if wy - d > 0 else 0,
                           wy + d + 1 if wy + d < MAP_DIM else MAP_DIM):
                bs.append(self.map.grid[x][y].building)

        for b in bs:
            if isinstance(b, House):
                if b.food < 6 * b.population:
                    # 1 year worth of food
                    food_wanted = 6 * b.population - b.food
                    sold = self.market.sell(food_wanted)
                    b.food += sold

    def can_go_back(self):
        return self.market.road_connection == self.map.grid[int(self.posx)][int(self.posy)].building and self.market.is_active() and self.market.road_connection is not None
