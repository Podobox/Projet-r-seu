import os
import sys
import sysv_ipc
import re
import pickle
import struct
from enum import Enum
# from Model.Player import Player

KEY = 1234
PY_TO_C = 2

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
        self.message_queue.send(message.encode(), type=PY_TO_C)

    def ask_for_money_ownership(self):
        message = struct.pack("iQQQQ", MessageType.REQUIRE_MONEY_OWNERSHIP, 0, 0, 0, 0)
        self.send_all(message)

    def ask_for_population_ownership(self):
        message = struct.pack("iQQQQ", MessageType.REQUIRE_POPULATION_OWNERSHIP, 0, 0, 0, 0)
        self.send_all(message)

    def build(self, posx, posy, type):
        message = struct.pack("iQQQQ", MessageType.BUILD, posx, posy, type, 0)
        self.send_all(message)

    def destroy(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DESTROY, posx, posy, 0, 0)
        self.send_all(message)

    def catch_fire(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.CATCH_FIRE, posx, posy, 0, 0)
        self.send_all(message)

    def put_out_fire(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.PUT_OUT_FIRE, posx, posy, 0, 0)
        self.send_all(message)

    def evolve(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.EVOLVE, posx, posy, 0, 0)
        self.send_all(message)

    def devolve(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DEVOLVE, posx, posy, 0, 0)
        self.send_all(message)

    def move_walker(self, posx, posy, building, walker_type):
        message = struct.pack("iQQQQ", MessageType.MOVE_WALKER, posx, posy, building,
                              walker_type)
        self.send_all(message)

    def ask_for_ownership(self, posx, posy, player, me):
        message = struct.pack("iQQQQ", MessageType.REQUIRE_OWNERSHIP, posx, posy, player, 0)
        self.send(message)
        # wait for answer and return
        message = struct.pack("iQQQQ", MessageType.CHANGE_OWNERSHIP, posx, posy, me, 0)
        self.send_all(message)

    def give_ownership(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.GIVE_OWNERSHIP, posx, posy, 0, 0)
        self.send(message)

    def check_messages(self):
        # check for messages from other players
        # making this function a generator might be a good idea
        # handle the message in the controller
        pass

    def connect(self, ip, port):
        message = struct.pack("iQQQQ", MessageType.CONNECT, ip, port, 0, 0)
        self.send(message)

        # return the game it is connected to and its players
        pass

    def diconnect(self):
        message = struct.pack("iQQQQ", MessageType.DISCONNECT, 0, 0, 0, 0)
        self.send_all(message)
        # cleanly disconnectand release all owned objects
        # if done well I believe the process is the same wether there are players still
        # connected or not
        pass

    def create(self):
        # create a game a make it available for others to connect
        # return the game
        # probably not the best file for this function
        pass

while (True):
    Sender = Communication()
    string = input("")
    Sender.send_message_from_py_to_c(string)
    if (str(string) == 'end' or str(string) == 'exit' or str(string) == ''):
        break
