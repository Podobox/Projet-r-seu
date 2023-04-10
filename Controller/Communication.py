import os
import socket
import subprocess
from time import time_ns
from enum import Enum
# from Model.Player import Player
import sys
import sysv_ipc
import re
import pickle
import struct
from queue import Queue
from time import sleep, time_ns
# import pygame
#from Model.Player import Player

ME = None


# if bug with population : add event for job offered in a specific building

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
    HOUSE_FOOD_STOCK = 26
    HOUSE_EAT = 27
    SPEND_MONEY = 28
    COLLECT_MONEY = 29
    # TODO below
    # change state of walkers ?


class Message(Enum):
    type: MessageType  # int
    posx: int  # llu
    posy: int  # llu
    playerID: int  # llu (or building depending on the message)
    add: int  # llu (additional field, walker_type)


class Communication:
    def __init__(self):
        sysv_ipc.MessageQueue.remove(sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT))
        # create fifo to communicate with c daemon
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT, mode=0o777)

        # try:
        #     # Try to create a new message queue with the same key
        #     self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT, mode=0o777)
        #     exists = False
        # except sysv_ipc.ExistentialError:
        #     # If the creation failed, return True
        #     exists = True
            
        # print(exists)

        self.message = Queue(-1)

    def send_message_from_py_to_c(self, message):
        # Convert message to bytes if necessary
        if not isinstance(message, bytes):
            message = message.encode()

        # Check message size
        if len(message) > 8192:
            return False

        # Send the message with the appropriate type
        try:
            self.message_queue.send(message, type=PY_TO_C)
            return True
        except sysv_ipc.BusyError:
            # Message queue is full, handle the error here
            return False
        except OSError as e:
            if e.errno == 22:
                # Invalid argument, handle the error here
                return False
            else:
                # Other OSError, re-raise the exception
                raise e

    def receive_message_from_c_to_py(self):
        # send the actions from c to python
        try:
            message, type = self.message_queue.receive(type=C_TO_PY, block=False)
            self.message.put(struct.unpack("iQQQQ", message))
            return True
        except sysv_ipc.BusyError:
            return False
        except sysv_ipc.ExistentialError:
            # Message queue no longer exists, handle the error here
            return False

    def receive_unique_message_from_c_to_py(self, id):
        # send the actions from c to python
        try:
            message, type = self.message_queue.receive(type=id, block=False)
            self.message.put(struct.unpack("iQQQQ", message))
            return True
        except sysv_ipc.BusyError:
            return False

    def spend_money(self, amount):
        message = struct.pack("iQQQQ", MessageType.SPEND_MONEY.value, 0, 0, amount, 0)
        # print('spend money :', message)
        self.send_message_from_py_to_c(message)

    def collect_money(self, amount):
        message = struct.pack("iQQQQ", MessageType.COLLECT_MONEY.value, 0, 0, amount, 0)
        self.send_message_from_py_to_c(message)

    def house_food_stock(self, posx, posy, stock):
        message = struct.pack("iQQQQ", MessageType.HOUSE_FOOD_STOCK.value, posx, posy, stock, 0)
        self.send_message_from_py_to_c(message)

    def house_eat(self, posx, posy, quantity):
        message = struct.pack("iQQQQ", MessageType.HOUSE_EAT.value, posx, posy, quantity, 0)
        self.send_message_from_py_to_c(message)

    def walker_destroy(self, posx, posy, walker_type):
        message = struct.pack("iQQQQ", MessageType.WALKER_DESTROY.value, posx, posy, 0, walker_type)
        self.send_message_from_py_to_c(message)

    def market_stock(self, posx, posy):
        # coordinates of the building the walker belongs to
        message = struct.pack("iQQQQ", MessageType.MARKET_STOCK.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def market_sell(self, posx, posy, quantity):
        # coordinates of the building the walker belongs to
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
        # coordinates of the building the walker belongs to
        message = struct.pack("iQQQQ", MessageType.GRANARY_UNSTOCK.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)

    def granary_stock(self, posx, posy):
        # coordinates of the building the walker belongs to
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

    def move_walker(self, posx, posy, walker_type, direction):  # TODO in Model
        message = struct.pack("iQQQQ", MessageType.MOVE_WALKER.value, posx, posy,
                              walker_type, direction)
        self.send_message_from_py_to_c(message)

    def ask_for_ownership(self, posx, posy, player, me):  # TODO in Model
        unique_id = time_ns()
        message = struct.pack("iQQQQ", MessageType.REQUIRE_OWNERSHIP.value, posx, posy,
                              player, unique_id)
        self.send_message_from_py_to_c(message)

        # TODO timeout ?
        while not self.receive_message_from_c_to_py(unique_id):
            message = struct.unpack("iQQQQ", self.message.get())
            if message[0] == MessageType.GIVE_OWNERSHIP.value and message[1] == posx \
                    and message[2] == posy and message[4] == unique_id:
                return
            else:
                assert False, f"clé unique identique: {message}"

    def give_ownership(self, posx, posy, unique_id):
        message = struct.pack("iQQQQ", MessageType.GIVE_OWNERSHIP.value, posx, posy, 0,
                              unique_id)
        self.send_message_from_py_to_c(message)

    def check_messages(self):
        # check for messages from other players
        # making this function a generator might be a good idea
        # handle the message in the controller

        while self.receive_message_from_c_to_py():
            yield self.message.get()
        return

    def accept_connect(self):
        message = struct.pack("iQQQQ", MessageType.CONNECT.value, 0, 0, 0, 0)
        self.send_message_from_py_to_c(message)

    def connect(self, ip, port):
        nom = "online_game"
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
        while self.receive_message_from_c_to_py():
            game = pickle.loads(self.message.get())
            return (nom, game)
        
        # return the game it is connected to and its players

        # If the loop did not run, return a default value
        return (nom, None)

    def disconnect(self, posx, posy):
        message = struct.pack("iQQQQ", MessageType.DISCONNECT.value, posx, posy, 0, 0)
        self.send_message_from_py_to_c(message)
        # cleanly disconnectand release all owned objects
        # if done well I believe the process is the same wether there are players still
        # connected or not
        pass


communication = Communication()

# """ TEST
# Sender = Communication()
# Sender.evolve(9, 5) #11
# Sender.devolve(9, 6) #12
# Sender.diconnect() #4
# Sender.connect(3, 8000) #3
# Sender.give_ownership(9, 7) #2
# Sender.move_walker(9, 8, 2, 3) #13
# Sender.put_out_fire(10, 9)
# """
# if (str(string) == 'end' or str(string) == 'exit' or str(string) == ''):
#     break

# Sender = Communication()
# Sender.burn_stage_increase(1, 1, 2)
# while (True):
    # for i in Sender.check_messages():
        # print(i)
    # sleep(1)
    # Sender.receive_message_from_c_to_py()
