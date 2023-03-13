from Model.Building import Building
from enum import Enum
from dataclasses import dataclass


class House_Level(Enum):
    # Keep the order , start at 1, step by 1 !!!
    # That way len(House_Level) == highest level
    # Changing would break evolving and devolving
    Small_Tent = 1
    Large_Tent = 2
    Small_Shack = 3
    Large_Shack = 4
    # ...


@dataclass
class House_Property:
    sizex: int
    sizey: int
    population: int
    des_init: int
    des_step: int
    des_step_size: int
    des_range: int
    evolve_at: int
    devolve_at: int
    tax_multiplier: int


house_property = {House_Level.Small_Tent: House_Property(1, 1, 5, -3, 1, 1, 3, -10, -99, 1),
                  House_Level.Large_Tent: House_Property(1, 1, 7, -3, 1, 1, 3, -5, -12,
                                                         1),
                  House_Level.Small_Shack: House_Property(1, 1, 9, -2, 1, 1, 2, 0, -7, 1),
                  House_Level.Large_Shack: House_Property(1, 1, 11, -2, 1, 1, 2, 4, -2, 1)
                  }


class House(Building):

    def __init__(self, tile):
        self.level = House_Level.Small_Tent
        self.population = house_property[self.level].population
        super().__init__(house_property[self.level].sizex,
                         house_property[self.level].sizey, tile, job_offered=0)
        self.food = 00
        self.last_taxe = None

    def __repr__(self):
        return self.level.name

    def evolve(self):
        if self.level.value == len(House_Level):
            # max level
            return 0

        if self.tile.desirability < house_property[self.level].evolve_at:
            return 0

        # water is needed after Small Tent
        if self.level.value >= House_Level.Small_Tent.value and not self.tile.water_coverage:
            return 0

        # food is needed after Large Tent
        if self.level.value >= House_Level.Large_Tent.value and self.food <= 0:
            return 0

        pop_buf = self.population
        self.level = House_Level(self.level.value + 1)
        self.population = house_property[self.level].population
        self.sizex = house_property[self.level].sizex
        self.sizey = house_property[self.level].sizey

        # print(f"evolved ({self.tile.posx}, {self.tile.posy}) to {self.level.name}")

        return self.population - pop_buf

    def devolve(self):
        if self.level == 1:
            # min level
            return 0

        if self.tile.desirability < house_property[self.level].devolve_at or \
                (self.level.value > House_Level.Small_Tent.value and not
                 self.tile.water_coverage) or \
                (self.level.value > House_Level.Large_Tent.value and self.food <= 0):
            pop_buf = self.population
            self.level = House_Level(self.level.value - 1)
            self.population = house_property[self.level].population
            self.sizex = house_property[self.level].sizex
            self.sizey = house_property[self.level].sizey
            return self.population - pop_buf

        return 0

    def eat(self):
        if self.level.value >= House_Level.Small_Shack.value and self.food > 0:
            print(f"eating {self.population} from {self.food} stock")
            for _ in range(self.population):
                self.food -= 1
            if self.food < 0:
                self.food = 0
