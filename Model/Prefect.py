from Model.Random_Walkers import Random_Walkers, Random_Walker_State
import Controller.Communication as com
from Model.Walkers import Action
from Model.Map import MAP_DIM
from enum import Enum


class Prefect_State(Enum):
    ROAMING = 1
    GOING_TO_FIRE = 2
    PUTING_OUT = 3
    RETURN = 4


class Prefect(Random_Walkers):

    def __init__(self, prefecture, spawn_road, map):
        # long patrol 52 tiles
        # short patrol 43 tiles
        super().__init__(52, 43, spawn_road, map)
        self.prefecture = prefecture
        self.building = prefecture
        self.prefect_state = Prefect_State.ROAMING
        self.puting_out = None
        self.puting_out_speed = 0.003  # stages per minutes

    def __repr__(self):
        return "Prefect"

    def find_destination(self, action):
        if self.prefect_state == Prefect_State.RETURN:
            self.destination = (self.prefecture.tile.posx, self.prefecture.tile.posy)
        elif self.prefect_state == Prefect_State.ROAMING:
            pass
        elif self.prefect_state == Prefect_State.GOING_TO_FIRE:
            self.prefect_state = Prefect_State.PUTING_OUT
        else:  # PUTING_OUT
            pass

    def action_while(self, date):
        # print(self.prefect_state)
        if self.prefect_state == Prefect_State.ROAMING or self.prefect_state == Prefect_State.RETURN:
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
                        if b.burning:
                            print("It's burning around !")
                            # TODO
                            self.puting_out = b
                            self.prefect_state = Prefect_State.GOING_TO_FIRE
                            self.destination = (b.tile.posx, b.tile.posy)
                            self.direction = None
                            return
                        b.burn_stage = 0
                        com.communication.burn_stage_reset(self.prefecture.tile.posx,
                                                           self.prefecture.tile.posy)
        elif self.prefect_state == Prefect_State.GOING_TO_FIRE:
            # print("prefect going to fire")
            pass
        else:  # PUTING_OUT
            # print("prefect puting out")
            water_amount = self.compute_water_amount(date)
            self.puting_out.burn_stage -= water_amount
            if self.puting_out.burn_stage < 0:
                self.puting_out.put_out_fire()
                self.prefect_state = Prefect_State.ROAMING
            pass

    def walk(self, date, action):
        if self.prefect_state == Prefect_State.RETURN:
            if action:
                self.action_while(date)
            if self.walk_to_destination(date):
                self.destination = None
                self.direction = None
                # self.state = Random_Walker_State.RANDOM
                self.prefect_state = Prefect_State.ROAMING
                # print("prefect going random")
                if action:
                    if self.can_go_back():
                        return Action.NONE
                    else:
                        return Action.DESTROY_SELF
        if self.prefect_state == Prefect_State.ROAMING:
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
                        # print("prefect returning")
                        # self.state = Random_Walker_State.RETURN
                        self.prefect_state = Prefect_State.RETURN
                        self.date_last_frame = date
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
                    # self.state = Random_Walker_State.RETURN
                    self.prefect_state = Prefect_State.RETURN

            self.date_last_frame = date
            if action:
                return self.action_while(date)
        elif self.prefect_state == Prefect_State.GOING_TO_FIRE:
            if self.walk_to_destination(date):
                self.prefect_state = Prefect_State.PUTING_OUT
            if action:
                self.action_while(date)
        else:  # PUTING_OUT
            if action:
                self.action_while(date)
            self.date_last_frame = date

    def can_go_back(self):
        return self.prefecture ==\
            self.map.grid[int(self.posx)][int(self.posy)].building and \
            self.prefecture.is_active() and self.prefecture.road_connection is not None

    def compute_water_amount(self, date):
        return (date - self.date_last_frame).total_seconds() / 60 * self.puting_out_speed
