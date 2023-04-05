from Model.Random_Walkers import Random_Walkers
from Model.House import House, house_property
from Model.Map import MAP_DIM

TAX_RATE = 10


class Tax_Collector(Random_Walkers):

    def __init__(self, forum, spawn_road, map):
        super().__init__(43, 35, spawn_road, map)
        self.forum = forum
        self.building = forum

    def __repr__(self):
        return "Tax_Collector"

    def find_destination(self):
        self.destination = (self.forum.road_connection.tile.posx,
                            self.forum.road_connection.tile.posy)

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
                if b.last_taxe is None or b.last_taxe < date.date().year:
                    b.last_taxe = date.date().year
                    tax = house_property[b.level].tax_multiplier * b.population / 17 * TAX_RATE
                    print(f"collecting {tax:.2} denarii from ({b.tile.posx}, {b.tile.posy})")
                    return tax
        return 0

    def can_go_back(self):
        return self.forum.road_connection == self.map.grid[int(self.posx)][int(self.posy)].building and self.forum.is_active() and self.forum.road_connection is not None
