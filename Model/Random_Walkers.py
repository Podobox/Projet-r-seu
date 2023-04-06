from Model.Walkers import Walkers, Action, Direction
from Model.Road import Road
from random import seed, random, choice
from enum import Enum


class Random_Walker_State(Enum):
    RANDOM = 1
    RETURN = 2


class Random_Walkers(Walkers):
    def __init__(self, long_patrol, short_patrol, spawn_road, map):
        super().__init__(map, spawn_road)
        self.long_patrol = long_patrol
        self.short_patrol = short_patrol
        self.long_patrol_probability = 1 / 4
        self.current_patrol = 0
        self.patrol_length = None
        self.state = Random_Walker_State.RANDOM
        self.last_direction = None

    def __repr__(self):
        return "Random_Walker"

    def __str__(self):
        string = super().__str__()
        string += f"{self.current_patrol}"
        return string

    def walk(self, date, action=True):
        if self.state == Random_Walker_State.RETURN:
            if self.walk_to_destination(date, action):
                self.destination = None
                self.last_direction = None
                self.direction = None
                self.state = Random_Walker_State.RANDOM
                # print("going random")
                if action:
                    if self.can_go_back():
                        return Action.NONE
                    else:
                        return Action.DESTROY_SELF
            if action:
                return self.action_while(date)
        else:  # RANDOM
            if self.date_last_frame is None:
                self.date_last_frame = date
                return

            if self.direction is None:
                if self.patrol_length is None:
                    self.choose_patrol()

                if action:
                    nt = self.find_next_tile(self.map)
                    if nt is None:
                        self.direction = None
                        # TODO reverse direction pour éviter de revenir a la base a chaque
                        # fois
                        self.current_patrol = 0
                        self.patrol_length = None
                        # print("returning")
                        self.state = Random_Walker_State.RETURN
                        return Action.NONE

                    self.find_direction(nt.posx, nt.posy)
                else:
                    return

            dist = self.compute_dist(date)

            middle_passed = self.move(dist)
            if middle_passed:
                self.current_patrol += 1
                self.last_direction = self.direction
                self.direction = None
                if self.current_patrol >= self.patrol_length:
                    self.current_patrol = 0
                    self.patrol_length = None
                    self.state = Random_Walker_State.RETURN

            self.date_last_frame = date
            return self.action_while(date)

    def choose_patrol(self):
        # seed()
        # p = random()
        # if p < self.long_patrol_probability:
            # self.patrol_length = self.long_patrol
        # else:
            # self.patrol_length = self.short_patrol
        # no sync needed
        self.patrol_length = self.short_patrol

    def find_next_tile(self, map):
        x = int(self.posx)
        y = int(self.posy)
        roads = []

        if self.last_direction != Direction.DOWN and map.is_type(x - 1, y, Road):
            roads.append(self.map.grid[x - 1][y].building)
        if self.last_direction != Direction.UP and map.is_type(x + 1, y, Road):
            roads.append(self.map.grid[x + 1][y].building)
        if self.last_direction != Direction.RIGHT and map.is_type(x, y - 1, Road):
            roads.append(self.map.grid[x][y - 1].building)
        if self.last_direction != Direction.LEFT and map.is_type(x, y + 1, Road):
            roads.append(self.map.grid[x][y + 1].building)

        if len(roads) == 0:
            return None

        return choice(roads).tile

    def find_destination(self):
        assert False, "virtual function call"

    def can_go_back(self):
        assert False, "virtual fuction call"

    def action_post(self):
        pass
