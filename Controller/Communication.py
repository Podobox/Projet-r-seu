import os
import socket
import subprocess
from enum import Enum
from Model.Player import Player
from Model.Engineer import Engineer
from Model.Farm_Boy import Farm_Boy
from Model.Market_Buyer import Market_Buyer
from Model.Market_Trader import Market_Trader
from Model.Migrant import Migrant
from Model.Prefect import Prefect
from Model.Tax_Collector import Tax_Collector
import sys
import sysv_ipc
import re
import pickle
import struct
# import pygame
#from Model.Player import Player

ME = None


def walker_type(w):
    walkers = [Engineer, Farm_Boy, Market_Buyer, Market_Trader, Migrant, Prefect, Tax_Collector]
    return walkers.index(w)


# if bug with population : add event for job offered in a specific building

KEY = 1234
PY_TO_C = 3
C_TO_PY = 99


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
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None

    def send_message_from_py_to_c(self, message):
        # send the actions from python to c
        self.message_queue.send(message, type=PY_TO_C) 

    def walker_destroy(self, posx, posy, walker_type):
        message = struct.pack("iQQQQ", MessageType.WALKER_DESTROY.value, posx, posy, 0, walker_type)
        self.send_message_from_py_to_c(message)

    def market_stock(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.MARKET_STOCK.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def market_sell(self, posx, posy, quantity):
        message = struct.pack("iQQQQ", MessageType.MARKET_STOCK.value, posx, posy,
                              quantity, 0)
        self.send_message_from_py_to_c(message)

    def burn_stage_reset(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.BURN_STAGE_RESET.value, posx, posy,
                              0, 0)
        self.send_message_from_py_to_c(message)

    def collapse_stage_reset(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.COLLAPSE_STAGE_RESET.value, posx, posy,
                              0, 0)
        self.send_message_from_py_to_c(message)

    def granary_unstock(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.GRANARY_UNSTOCK.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def granary_stock(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.GRANARY_STOCK.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def walker_spawn(self, posx, posy, walker_type):
        message = struct.pack("iQQQQ", MessageType.WALKER_SPAWN.value, posx, posy, 0,
                              walker_type)
        self.send_message_from_py_to_c(message)

    def burn_stage_increase(self, posx, posy, level):
        message = struct.pack("iQQQQ", MessageType.BURN_STAGE_INCREASE.value, posx, posy, level, 0)
        self.send_message_from_py_to_c(message)

    def collapse_stage_increase(self, posx, posy, level):
        message = struct.pack(
            "iQQQQ", MessageType.COLLAPSE_STAGE_INCREASE.value, posx, posy, level, 0)
        self.send_message_from_py_to_c(message)

    def ask_for_money_ownership(self):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.REQUIRE_MONEY_OWNERSHIP.value, 0, 0, 0, 0)
        self.send_message_from_py_to_c(message)

    def ask_for_population_ownership(self):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.REQUIRE_POPULATION_OWNERSHIP.value, 0, 0, 0, 0)
        self.send_message_from_py_to_c(message)

    def build(self, posx, posy, type):
        message = struct.pack("iQQQQ", MessageType.BUILD.value, posx, posy, type, 0)
        self.send_message_from_py_to_c(message)

    def destroy(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DESTROY.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def catch_fire(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.CATCH_FIRE.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def put_out_fire(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.PUT_OUT_FIRE.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def evolve(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.EVOLVE.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def devolve(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DEVOLVE.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def move_walker(self, posx, posy, building, walker_type):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.MOVE_WALKER.value, posx, posy, building,
                              walker_type)
        self.send_message_from_py_to_c(message)

    def ask_for_ownership(self, posx, posy, player, me):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.REQUIRE_OWNERSHIP.value, posx, posy, player, 0)
        self.send_message_from_py_to_c(message)
        # wait for answer and return
        message = struct.pack("iQQQQ", MessageType.CHANGE_OWNERSHIP.value, posx, posy, me, 0)
        self.send_message_from_py_to_c(message)

    def give_ownership(self, posx, posy):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.GIVE_OWNERSHIP.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def check_messages(self):
        # check for messages from other players
        # making this function a generator might be a good idea
        # handle the message in the controller
        yield (MessageType.DESTROY.value, 9, 9, 0, 0)
        return

    def connect(self, ip, port):
        try:
            message = struct.pack("i4sIQQ", MessageType.CONNECT.value, socket.inet_aton(ip), int(port), 0, 0)
        except struct.error as e:
            raise ValueError(f"Error packing message: {e}")  
        
        # Define the command to run
        cmd = ["./c_daemon/bin/c_daemon", ip, str(port)]

        # Start the process
        process = subprocess.Popen(cmd)
       
        self.send_message_from_py_to_c(message)

        # wait for response from c daemon and unpack the game and player information
        response, _ = self.message_queue.receive(type=C_TO_PY)
        game, players = struct.unpack("iQ", response)
        print(game, players)

        return game, players
   
        # return the game it is connected to and its players 
        # pass

    def disconnect(self):
        message = struct.pack("iQQQQ", MessageType.DISCONNECT.value, 0, 0, 0, 0)
        self.send_message_from_py_to_c(message)
        # cleanly disconnectand release all owned objects
        # if done well I believe the process is the same wether there are players still
        # connected or not
        pass

    def create(self):
        # create a game a make it available for others to connect
        # return the game
        # probably not the best file for this function
        pass

""" TEST
Sender = Communication() 
Sender.evolve(9, 5) #11
Sender.devolve(9, 6) #12
Sender.diconnect() #4
Sender.connect(3, 8000) #3
Sender.give_ownership(9, 7) #2
Sender.move_walker(9, 8, 2, 3) #13
Sender.put_out_fire(10, 9)
"""
# if (str(string) == 'end' or str(string) == 'exit' or str(string) == ''):
#     break
