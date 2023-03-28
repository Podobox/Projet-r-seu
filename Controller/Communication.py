import os
import pickle
import struct
from enum import Enum
from Model.Player import Player
from Model.Engineer import Engineer
from Model.Farm_Boy import Farm_Boy
from Model.Market_Buyer import Market_Buyer
from Model.Market_Trader import Market_Trader
from Model.Migrant import Migrant
from Model.Prefect import Prefect
from Model.Tax_Collector import Tax_Collector

ME = None


def walker_type(w):
    walkers = [Engineer, Farm_Boy, Market_Buyer, Market_Trader, Migrant, Prefect, Tax_Collector]
    return walkers.index(w)


# if bug with population : add event for job offered in a specific building
class MessageType(Enum):
    REQUIRE_OWNERSHIP = 1
    GIVE_OWNERSHIP = 2
    CONNECT = 3
    DISCONNECT = 4
    ACCEPT_CONNECTION = 5
    CHANGE_OWNERSHIP = 6
    BUILD = 7
    DESTROY = 8
    CATCH_FIRE = 9
    PUT_OUT_FIRE = 10
    EVOLVE = 11
    DEVOLVE = 12
    MOVE_WALKER = 13
    REQUIRE_MONEY_OWNERSHIP = 14
    REQUIRE_POPULATION_OWNERSHIP = 15
    BURN_STAGE_INCREASE = 16
    COLLAPSE_STAGE_INCREASE = 17
    WALKER_SPAWN = 18
    GRANARY_STOCK = 19
    GRANARY_UNSTOCK = 20
    COLLAPSE_STAGE_RESET = 21
    BURN_STAGE_RESET = 22
    MARKET_STOCK = 23
    MARKET_SELL = 24
    # TODO below
    WALKER_DESTROY = 25



class Message(Enum):
    type: MessageType  # int
    posx: int  # llu
    posy: int  # llu
    playerID: int  # llu (or building depending on the message)
    add: int  # llu (additional field, walker_type)


class Communication:
    def __init__(self):
        # create fifo to communicate with c daemon
        self.fifo = ...

    def send(self, message):
        pass

    def walker_destroy(self, posx, posy, walker_type):
        message = struct.pack("iQQQQ", MessageType.WALKER_DESTROY, posx, posy, 0, walker_type)
        self.send(message)

    def market_stock(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.MARKET_STOCK.value, posx, posy, 0, 0)
        self.send(message)

    def market_sell(self, posx, posy, quantity):
        message = struct.pack("iQQQQ", MessageType.MARKET_STOCK.value, posx, posy,
                              quantity, 0)
        self.send(message)

    def burn_stage_reset(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.BURN_STAGE_RESET, posx, posy,
                              0, 0)
        self.send(message)

    def collapse_stage_reset(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.COLLAPSE_STAGE_RESET, posx, posy,
                              0, 0)
        self.send(message)

    def granary_unstock(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.GRANARY_UNSTOCK.value, posx, posy, 0, 0)
        self.send(message)

    def granary_stock(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.GRANARY_STOCK.value, posx, posy, 0, 0)
        self.send(message)

    def walker_spawn(self, posx, posy, walker_type):
        message = struct.pack("iQQQQ", MessageType.WALKER_SPAWN, posx, posy, 0,
                              walker_type)
        self.send(message)

    def burn_stage_increase(self, posx, posy, level):
        message = struct.pack("iQQQQ", MessageType.BURN_STAGE_INCREASE.value, posx, posy, level, 0)
        self.send(message)

    def collapse_stage_increase(self, posx, posy, level):
        message = struct.pack(
            "iQQQQ", MessageType.COLLAPSE_STAGE_INCREASE.value, posx, posy, level, 0)
        self.send(message)

    def ask_for_money_ownership(self):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.REQUIRE_MONEY_OWNERSHIP.value, 0, 0, 0, 0)
        self.send(message)

    def ask_for_population_ownership(self):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.REQUIRE_POPULATION_OWNERSHIP.value, 0, 0, 0, 0)
        self.send(message)

    def build(self, posx, posy, type):
        message = struct.pack("iQQQQ", MessageType.BUILD.value, posx, posy, type, 0)
        self.send(message)

    def destroy(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DESTROY.value, posx, posy, 0, 0)
        self.send(message)

    def catch_fire(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.CATCH_FIRE.value, posx, posy, 0, 0)
        self.send(message)

    def put_out_fire(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.PUT_OUT_FIRE.value, posx, posy, 0, 0)
        self.send(message)

    def evolve(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.EVOLVE.value, posx, posy, 0, 0)
        self.send(message)

    def devolve(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DEVOLVE.value, posx, posy, 0, 0)
        self.send(message)

    def move_walker(self, posx, posy, building, walker_type):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.MOVE_WALKER.value, posx, posy, building,
                              walker_type)
        self.send(message)

    def ask_for_ownership(self, posx, posy, player, me):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.REQUIRE_OWNERSHIP.value, posx, posy, player, 0)
        self.send(message)
        # wait for answer and return
        message = struct.pack("iQQQQ", MessageType.CHANGE_OWNERSHIP.value, posx, posy, me, 0)
        self.send(message)

    def give_ownership(self, posx, posy):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.GIVE_OWNERSHIP.value, posx, posy, 0, 0)
        self.send(message)

    def check_messages(self):
        # check for messages from other players
        # making this function a generator might be a good idea
        # handle the message in the controller
        pass

    def connect(self, ip, port):
        message = struct.pack("iQQQQ", MessageType.CONNECT.value, ip, port, 0, 0)
        self.send(message)

        # return the game it is connected to and its players
        pass

    def diconnect(self):
        message = struct.pack("iQQQQ", MessageType.DISCONNECT.value, 0, 0, 0, 0)
        self.send(message)
        # cleanly disconnectand release all owned objects
        # if done well I believe the process is the same wether there are players still
        # connected or not
        pass

    def create(self):
        # create a game a make it available for others to connect
        # return the game
        # probably not the best file for this function
        pass
