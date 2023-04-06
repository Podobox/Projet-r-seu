import os
import sys
import sysv_ipc
import re
import pickle
import struct
import pygame
from enum import Enum
#from Model.Player import Player

KEY = 1234
PY_TO_C = 3
C_TO_PY = 2

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


# class Message(Enum):
#     type: MessageType  # int
#     posx: int  # llu
#     posy: int  # llu
#     playerID: int  # llu (or building depending on the message)
#     add: int  # llu (additional field, walker_type)


class Communication:
    def __init__(self):
        # create fifo to communicate with c daemon
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None

    def send_message_from_py_to_c(self, message):
        # send the actions from python to c
        self.message_queue.send(message, type=PY_TO_C)

    def receive_message_from_c_to_py(self):
        # send the actions from c to python
        message = self.message_queue.receive(type=C_TO_PY)
        print(struct.unpack("iQQQQ", message.decode()))
     
    def ask_for_money_ownership(self):
        message = struct.pack("iQQQQ", MessageType.REQUIRE_MONEY_OWNERSHIP, 0, 0, 0, 0)
        self.send_message_from_py_to_c(message)

    def ask_for_population_ownership(self):
        message = struct.pack("iQQQQ", MessageType.REQUIRE_POPULATION_OWNERSHIP, 0, 0, 0, 0)
        self.send_message_from_py_to_c(message)

    def build(self, posx, posy, type):
        message = struct.pack("iQQQQ", MessageType.BUILD, posx, posy, type, 0)
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

    def move_walker(self, posx, posy, building, walker_type):
        message = struct.pack("iQQQQ", MessageType.MOVE_WALKER.value, posx, posy, building,
                              walker_type)
        self.send_message_from_py_to_c(message)

    def ask_for_ownership(self, posx, posy, player, me):
        message = struct.pack("iQQQQ", MessageType.REQUIRE_OWNERSHIP, posx, posy, player, 0)
        self.send_message_from_py_to_c(message)
        # wait for answer and return
        message = struct.pack("iQQQQ", MessageType.CHANGE_OWNERSHIP, posx, posy, me, 0)
        self.send_message_from_py_to_c(message)

    def give_ownership(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.GIVE_OWNERSHIP.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def check_messages(self):
        # check for messages from other players
        # making this function a generator might be a good idea
        # handle the message in the controller
        pass

    def connect(self, ip, port):
        message = struct.pack("iQQQQ", MessageType.CONNECT.value, ip, port, 0, 0)
        self.send_message_from_py_to_c(message)

        # return the game it is connected to and its players
        pass

    def diconnect(self):
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



Sender = Communication() 
Sender.evolve(9, 5) #11
Sender.devolve(9, 6) #12
Sender.diconnect() #4
Sender.connect(3, 8000) #3
Sender.give_ownership(9, 7) #2
Sender.move_walker(9, 8, 2, 3) #13
Sender.put_out_fire(10, 9)

while (True):
    Sender.receive_message_from_c_to_py()


