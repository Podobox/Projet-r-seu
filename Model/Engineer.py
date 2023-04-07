from Model.Random_Walkers import Random_Walkers
from Model.Map import MAP_DIM


class Engineer(Random_Walkers):

    def __init__(self, post, spawn_road, map):
        # long patrol 52 tiles
        # short patrol 43 tiles
        super().__init__(52, 43, spawn_road, map)
        self.post = post
        self.building = post

    def __repr__(self):
        return "Engineer"

    def find_destination(self, action):
        self.destination = (self.post.tile.posx, self.post.tile.posy)

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
            if b is not None:
                b.collapse_stage = 0
                self.post.communication.collapse_stage_reset(self.post.tile.posx,
                                                             self.post.tile.posy)

    def can_go_back(self):
        return self.post == self.map.grid[int(self.posx)][int(self.posy)].building and self.post.is_active() and self.post.road_connection is not None
