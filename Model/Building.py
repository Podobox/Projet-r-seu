from datetime import timedelta
from math import floor
from random import random


COLLAPSE_PROBABILITY = 0.0005
BURN_PROBABILITY = 0.0005

# Bonne version
STAGES_BEFORE_BURN = 10
STAGES_BEFORE_COLLAPSE = 10

# in hours
BURNING_TIME_BEFORE_COLLAPSE = 20 * 24
# test value
# BURNING_TIME_BEFORE_COLLAPSE = 5*24*1000000


class Building:

    def __init__(self, sizex, sizey, tile, job_offered):
        self.sizex = sizex
        self.sizey = sizey
        self.tile = tile
        self.burn_stage = 0
        self.collapse_stage = 0
        # self.posx = posx
        # self.posy = posy
        self.employees = 0
        self.job_offered = job_offered
        # ONE of the road by which the building is connected, None if not connected
        self.road_connection = None
        self.burning = False
        self.burning_start = None
        self.collapsed = False
        # Added to cover the full building like the real game - Tuan
        self.water_coverage = False
        self.communication = None  # will be set by Game

    def __str__(self):
        string = self.__repr__()
        string += f" ({self.tile.posx}, {self.tile.posy})"
        string += f"\n\tBurn stage: {self.burn_stage}"
        string += f"\n\tCollapse stage: {self.collapse_stage}"
        string += f"\n\tJobs: {self.employees}/{self.job_offered}"
        string += "\n\tRoad connections: "
        if self.road_connection:
            string += f"({self.road_connection.tile.posx},{self.road_connection.tile.posy})"
        else:
            string += "None"
        return string

    # return True if collapsing, else False
    def burn(self, time, multiplier):
        if not self.burning:
            f = floor(multiplier)
            bs_buf = self.burn_stage
            for _ in range(f):
                self.burn_stage += 1 if random() > (1 - BURN_PROBABILITY) else 0
            if random() < multiplier - f:
                self.burn_stage += 1 if random() > (1 - BURN_PROBABILITY) else 0
            if self.burn_stage != bs_buf:
                self.communication.burn_stage_increase(self.tile.posx, self.tile.posy,
                                                       self.burn_stage)

            if self.burn_stage > STAGES_BEFORE_BURN:
                self.catch_fire(time)
        else:
            if time - self.burning_start > timedelta(hours=BURNING_TIME_BEFORE_COLLAPSE):
                return True

        return False

    def catch_fire(self, time, com=True):
        self.burning = True
        self.burning_start = time
        if com:
            self.communication.catch_fire(self.tile.posx, self.tile.posy)

    def put_out_fire(self, com=True):
        self.burning = False
        self.burning_start = None
        self.burn_stage = 0
        if com:
            self.communication.put_out_fire(self.tile.posx, self.tile.posy)

    # return True if collapsing, else False
    def collapse(self, multiplier):
        f = floor(multiplier)
        cs_buf = self.collapse_stage
        for _ in range(f):
            self.collapse_stage += 1 if random() > (1 - COLLAPSE_PROBABILITY) else 0
        if random() < multiplier - f:
            self.collapse_stage += 1 if random() > (1 - COLLAPSE_PROBABILITY) else 0
        if self.collapse_stage != cs_buf:
            self.communication.collapse_stage_increase(self.tile.posx, self.tile.posy,
                                                       self.collapse_stage)

        return self.collapse_stage > STAGES_BEFORE_COLLAPSE

    def is_active(self):
        return self.employees == self.job_offered and self.road_connection is not None

    def offer_jobs(self):
        return self.employees < self.job_offered
