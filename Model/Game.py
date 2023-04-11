from Model.Collapsed import Collapsed
from Model.Engineer_Post import Engineer_Post
from Model.Forum import Forum
from Model.Fountain import Fountain
from Model.Garden import Garden
from Model.Granary import Granary

from Model.House import House, house_property
from Model.Market import Market
from Model.New_House import New_House
from Model.Other_Rock import Other_Rock
from Model.Prefecture import Prefecture
from Model.Road import Road
from Model.Rock import Rock
from Model.Senate import Senate
from Model.Tree import Tree
from Model.Water import Water
from Model.Well import Well
from Model.Wheat_Farm import Wheat_Farm
from Model.Sign import Sign, Sign_Type
from Model.Migrant import Migrant
from Model.Walkers import Action

from Model.Engineer import Engineer
from Model.Farm_Boy import Farm_Boy
from Model.Tax_Collector import Tax_Collector
from Model.Market_Buyer import Market_Buyer
from Model.Market_Trader import Market_Trader
from Model.Prefect import Prefect, Prefect_State
from Model.Random_Walkers import Random_Walkers, Random_Walker_State

from Model.Map import Map, MAP_DIM
from Model.Models_Data import building_data
from Model.Tile import Tile_Type
from random import seed, randint
from datetime import datetime, timedelta
import Controller.Communication as com


# min par frame
TIME_PER_FRAME = 10


def building_type(b, to_num=True):
    buildings = [Collapsed, Engineer_Post, Forum, Fountain, Garden, Granary, House,
                 Market, New_House, Prefecture, Road, Senate, Well, Wheat_Farm]
    if to_num:
        return buildings.index(b)
    else:
        return buildings[b]


def walker_type(w, to_num=True):
    walkers = [Engineer, Farm_Boy, Market_Buyer, Market_Trader, Migrant, Prefect, Tax_Collector]
    if to_num:
        return walkers.index(w)
    else:
        return walkers[w]


class Game:

    def __init__(self, denarii):
        self.map = Map()
        self.denarii = denarii
        self.population = 0
        self.unemployed = 0
        self.walkers = []
        self.buildings = []
        self.date = datetime(1, 1, 1)
        self.paused = False
        self.speed = 1  # speed scaling
        self.last_meal = self.date

    def __str__(self):
        string = str(self.map)
        string += f"\nSpeed: {self.speed}"
        string += f"\nPaused: {self.paused}"
        string += f"\nDenarii: {self.denarii}"
        string += f"\nUnemployed: {self.unemployed}/{self.population}"
        for w in self.walkers:
            string += f"\n{w}"
        for b in self.buildings:
            string += f"\n{b}"
        return string

    def set_initial_map(self):
        for y in range(0, MAP_DIM - MAP_DIM // 5):
            for x in range(y // 2):
                self.build(x, y, Water)
        self.set_entry_point(MAP_DIM // 2, 0)
        self.set_exit_point(MAP_DIM // 2, MAP_DIM - 1)
        x = MAP_DIM // 2
        for y in range(0, MAP_DIM):
            self.build(x, y, Road)
        for y in range(0, MAP_DIM):
            x = randint(3 * MAP_DIM // 4, MAP_DIM)
            self.build(x, y, Other_Rock)
        for x in range(MAP_DIM, 3 * MAP_DIM // 4, -1):
            # self.game.build(x, x-5, Rock)
            m = randint(0, MAP_DIM // 4)
            self.build(x, m // 2, Rock)
        for x in range(0, MAP_DIM):
            m = randint(0, MAP_DIM // 4)
            self.build(m, m // 2, Rock)

        for x in range(0, MAP_DIM):
            # y = random.randint(0, MAP_DIM)
            for y in range(0, MAP_DIM):
                self.build(x, y, Tree)

    def take_all_ownership(self, player):
        self.map.take_all_ownership(player)

    # return True if it was payed, else False
    def pay(self, price):
        if self.denarii >= price:
            if price == 0:
                return True
            self.denarii -= price
            com.communication.spend_money(price)
            return True
        return False

    def set_entry_point(self, posx, posy):
        self.build(posx, posy, Sign)
        building = self.map.grid[posx][posy].building
        if building is None or not isinstance(building, Sign):
            return

        building.set_type(Sign_Type.Enter)
        self.map.entry_point = building

    def set_exit_point(self, posx, posy):
        self.build(posx, posy, Sign)
        building = self.map.grid[posx][posy].building
        if building is None or not isinstance(building, Sign):
            return

        building.set_type(Sign_Type.Exit)
        self.map.exit_point = building

    def build(self, posx, posy, type, force=False):
        # only happen when adding buildings
        assert type in building_data, "type to build not in 'model_data'"

        # check emptiness of the tile
        b = type(None)
        startx = int(posx - b.sizex / 2) + 1 if posx - b.sizex / 2 > 0 else 0
        endx = int(posx + b.sizex / 2) + 1
        for x in range(startx, endx):
            starty = int(posy - b.sizey / 2) + 1 if posy - b.sizey / 2 > 0 else 0
            endy = int(posy + b.sizey / 2) + 1
            for y in range(starty, endy):
                if not self.map.is_type(x, y, None):
                    return

        if type in (Engineer_Post, Forum, Fountain, Garden, Granary, Market, New_House,
                    Prefecture, Road, Senate, Well, Sign)\
                and self.map.grid[posx][posy].type not in (Tile_Type.Field, Tile_Type.Grass):
            return

        if type in (Wheat_Farm,) and self.map.grid[posx][posy].type not in (Tile_Type.Field,):
            return

        if not force and not self.pay(building_data[type].price):
            return

        self.map.build(posx, posy, type)
        # print(self.map)

        building = self.map.grid[posx][posy].building

        if type == House:
            additional_population = building.population
            self.population += additional_population
            self.unemployed += additional_population

        if type == Road:
            # check every building for road connection
            self.road_connect()
        else:
            # only check for the new building because it doesn't impact the others
            self.road_connect([building])

        self.buildings.append(building)

        if not force and type not in (Water, Tree, Rock, Other_Rock, Sign):
            com.communication.build(posx, posy, building_type(type))

    def destroy(self, posx, posy, force=False):
        building = self.map.grid[posx][posy].building
        if building is None:
            return

        if isinstance(building, Sign):
            return

        building_type = type(building)
        if building_type == Rock or building_type == Water or building_type == Other_Rock:
            return

        if not force and not self.pay(2):
            return

        if building_type == House:
            removed_population = building.population
            self.population -= removed_population
            self.unemployed -= removed_population
            m = Migrant(self.map, building, self.map.exit_point, leaving=True)
            self.walkers.append(m)
        self.unemployed += building.employees

        if isinstance(building, Engineer_Post) and building.engineer is not None:
            self.remove_from_walkers(building.engineer)
        elif isinstance(building, Wheat_Farm) and building.farm_boy is not None:
            self.remove_from_walkers(building.farm_boy)
        elif isinstance(building, Forum) and building.tax_collector is not None:
            self.remove_from_walkers(building.tax_collector)
        elif isinstance(building, Market):
            if building.buyer is not None:
                self.remove_from_walkers(building.buyer)
            if building.trader is not None:
                self.remove_from_walkers(building.trader)
        elif isinstance(building, Prefecture) and building.prefect is not None:
            self.remove_from_walkers(building.prefect)

        self.buildings.remove(building)

        self.map.destroy(posx, posy)

        if building_type == Road:
            self.road_connect()

        if not force:
            com.communication.destroy(posx, posy)

    def job_hunt(self):
        if self.unemployed < 0:
            # a house got destroyed and its inhabitant were working, we need to
            # remove them inhabitants from where they were working
            for b in reversed(self.buildings):
                if self.unemployed == 0:
                    break
                if b.employees > 0:
                    new_unemployed = b.employees \
                        if b.employees < -self.unemployed else -self.unemployed
                    b.employees -= new_unemployed
                    self.unemployed += new_unemployed
        else:
            # we have unemployed peoples, let's search if they can work anywhere
            for b in self.buildings:
                if self.unemployed == 0:
                    break
                if b.offer_jobs():
                    new_employees = b.job_offered - b.employees if b.job_offered -\
                        b.employees <= self.unemployed else self.unemployed
                    b.employees += new_employees
                    self.unemployed -= new_employees

    def road_connect(self, buildings=None):
        # hack because we can't use 'self' in the default value
        if buildings is None:
            buildings = self.buildings
        # print(buildings)
        for b in buildings:
            if isinstance(b, Road):
                continue
            b.road_connection = self.map.road_connection(b)

    def burn(self):
        seed()  # random.seed
        for b in self.buildings:
            if isinstance(b, Road) or isinstance(b, Collapsed) or \
                    isinstance(b, Other_Rock) or isinstance(b, Rock) or \
                    isinstance(b, Tree) or isinstance(b, Water) or \
                    isinstance(b, New_House) or isinstance(b, House) or \
                    isinstance(b, Sign) or isinstance(b, Prefecture) or \
                    isinstance(b, Well) or isinstance(b, Fountain) or \
                    b.tile.owner != com.ME:
                continue
            if b.burn(self.date, self.speed):
                posx, posy = b.tile.posx, b.tile.posy
                self.destroy(posx, posy)
                startx = int(posx - b.sizex / 2) + 1 if posx - b.sizex / 2 > 0 else 0
                endx = int(posx + b.sizex / 2) + 1
                for x in range(startx, endx):
                    starty = int(posy - b.sizey / 2) + 1 if posy - b.sizey / 2 > 0 else 0
                    endy = int(posy + b.sizey / 2) + 1
                    for y in range(starty, endy):
                        self.build(x, y, Collapsed)

    def collapse(self):
        seed()  # random.seed
        for b in self.buildings:

            if isinstance(b, Road) or isinstance(b, Collapsed) or \
                    isinstance(b, Other_Rock) or isinstance(b, Tree) or \
                    isinstance(b, Water) or isinstance(b, Rock) or \
                    isinstance(b, Sign) or isinstance(b, House) or \
                    isinstance(b, New_House) or isinstance(b, Engineer_Post):
                continue
            if b.collapse(self.speed):
                posx, posy = b.tile.posx, b.tile.posy
                self.destroy(posx, posy)
                startx = int(posx - b.sizex / 2) + 1 if posx - b.sizex / 2 > 0 else 0
                endx = int(posx + b.sizex / 2) + 1
                for x in range(startx, endx):
                    starty = int(posy - b.sizey / 2) + 1 if posy - b.sizey / 2 > 0 else 0
                    endy = int(posy + b.sizey / 2) + 1
                    for y in range(starty, endy):
                        self.build(x, y, Collapsed)

    def eat(self):
        # workers eat 6 units of food a year
        if (self.date - self.last_meal) >= timedelta(days=365 / 6):
            self.last_meal = self.date
            for b in self.buildings:
                if isinstance(b, House) and b.tile.owner is com.ME:
                    b.eat()

    def farm(self):
        for b in self.buildings:
            if isinstance(b, Wheat_Farm) and b.tile.owner is com.ME:
                b.farm(self.date)
                buf = b.farm_boy
                if b.deliver(self.map):
                    self.add_to_walkers(b.farm_boy)
                elif b.farm_boy is None and buf is not None:
                    self.remove_from_walkers(buf)

    def advance_time(self):
        delta = timedelta(minutes=TIME_PER_FRAME)
        self.date += delta * self.speed

    def pause(self):
        if self.paused:
            self.speed = self.paused
            self.paused = False
            print("unpause")
        else:
            #self.speed = self.paused
            self.paused = self.speed
            self.speed = 0
            print("pause")

    def increase_speed(self):
        if self.speed > 5:
            return
        if self.speed < 1.95:
            self.speed += 0.1
        else:
            self.speed += 0.5

    def decrease_speed(self):
        if self.speed < 0.15:  # speed == 0.1 but with float
            return
        elif self.speed < 2.05:
            self.speed -= 0.1
        else:
            self.speed -= 0.5

    # TODO move in map.py
    def compute_desirability(self):
        for x in self.map.grid:
            for y in x:
                y.desirability = 0
        for b in self.buildings:
            data = building_data[type(b)]
            if isinstance(b, House):
                des_init = house_property[b.level].des_init
                des_step = house_property[b.level].des_step
                des_step_size = house_property[b.level].des_step_size
                des_range = house_property[b.level].des_range
            elif data.des_range == 0 or data.des_step_size == 0 or data.des_step == 0:
                continue
            else:
                des_init = data.des_init
                des_step = data.des_step
                # negative step size means all the same
                des_step_size = data.des_step_size if data.des_step_size > 0 else \
                    data.des_range + 1
                des_range = data.des_range
            for x in range(b.tile.posx - des_range, b.tile.posx + des_range + 1):
                if x < 0 or x >= MAP_DIM:
                    continue
                for y in range(b.tile.posy - des_range, b.tile.posy + des_range + 1):
                    if y < 0 or y >= MAP_DIM:
                        continue
                    self.map.grid[x][y].desirability += des_init + des_step * \
                        (max(abs(x - b.tile.posx), abs(y - b.tile.posy)) // des_step_size)

    def check_evolution(self):
        for b in self.buildings:
            if isinstance(b, House) and b.tile.owner is com.ME:
                diff = b.evolve()
                if diff != 0:
                    com.communication.evolve(b.tile.posx, b.tile.posy)
                self.population += diff
                self.unemployed += diff
                diff = b.devolve()
                if diff != 0:
                    com.communication.devolve(b.tile.posx, b.tile.posy)
                self.population += diff
                self.unemployed += diff
            elif isinstance(b, New_House) and b.tile.owner is com.ME:
                if self.map.entry_point is not None and b.migrate(self.map):
                    com.communication.walker_spawn(self.map.entry_point.tile.posx,
                                                   self.map.entry_point.tile.posy,
                                                   walker_type(Migrant))
                    self.add_to_walkers(b.migrant)

    def fill_market(self):
        for b in self.buildings:
            if isinstance(b, Market) and b.tile.owner is com.ME:
                buf = b.buyer
                if b.fill(self.map):
                    self.add_to_walkers(b.buyer)
                elif b.buyer is None and buf is not None:
                    self.remove_from_walkers(buf)

    def trade_market(self):
        for b in self.buildings:
            if isinstance(b, Market) and b.tile.owner is com.ME:
                buf = b.trader
                if b.trade(self.map):
                    self.add_to_walkers(b.trader)
                elif b.trader is None and buf is not None:
                    self.remove_from_walkers(buf)

    def walk(self):
        for w in self.walkers:
            if w.building.tile.owner != com.ME:
                if isinstance(w, Random_Walkers) and w.state == Random_Walker_State.RANDOM:
                    continue
                if isinstance(w, Prefect) and w.prefect_state != Prefect_State.RETURN:
                    continue
            # print(w.building.tile, com.ME)
            res = w.walk(self.date, action=(w.building.tile.owner == com.ME))
            if w.building.tile.owner == com.ME:
                match res:
                    case Action.NONE: pass
                    case Action.BUILD_HOUSE:
                        self.denarii += 2
                        com.communication.collect_money(2)
                        x, y = w.house.tile.posx, w.house.tile.posy
                        self.destroy(x, y)
                        self.build(x, y, House)
                        self.remove_from_walkers(w)
                    case Action.DESTROY_SELF:
                        match w:
                            case Market_Buyer():
                                w.market.buyer = None
                            case Migrant():
                                w.house.migrant = None
                            case Farm_Boy():
                                w.farm.farm.boy = None
                            case Engineer():
                                w.post.engineer = None
                        self.remove_from_walkers(w)
                    case _:
                        if isinstance(w, Tax_Collector) and type(res) is float:
                            self.denarii += int(res)
                            com.communication.collect_money(int(res))
                            print(f"new balance: {self.denarii}")

    def engineer(self):
        for b in self.buildings:
            if isinstance(b, Engineer_Post) and b.tile.owner is com.ME:
                buf = b.engineer
                if b.engineer_do(self.map):
                    self.add_to_walkers(b.engineer)
                elif b.engineer is None and buf is not None:
                    self.remove_from_walkers(buf)

    def firefight(self):
        for b in self.buildings:
            if isinstance(b, Prefecture) and b.tile.owner is com.ME:
                buf = b.prefect
                if b.prefect_do(self.map):
                    self.add_to_walkers(b.prefect)
                elif b.prefect is None and buf is not None:
                    self.remove_from_walkers(buf)

    def collect_tax(self):
        for b in self.buildings:
            if isinstance(b, Forum) and b.tile.owner is com.ME:
                buf = b.tax_collector
                if b.collect(self.map):
                    self.add_to_walkers(b.tax_collector)
                elif b.tax_collector is None and buf is not None:
                    self.remove_from_walkers(buf)

    def get_denarii(self):
        return self.denarii

    def add_to_walkers(self, w):
        self.walkers.append(w)
        self.walkers.sort(key=lambda w: w.posy + w.posx)
        com.communication.walker_spawn(w.building.tile.posx, w.building.tile.posy,
                                       walker_type(type(w)))

    def remove_from_walkers(self, w):
        self.walkers.remove(w)
        com.communication.walker_destroy(w.building.tile.posx,
                                         w.building.tile.posy,
                                         walker_type(type(w)))
