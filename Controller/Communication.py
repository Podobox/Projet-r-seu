import os


class Communication:
    def __init__(self):
        # create fifo to communicate with c daemon
        self.fifo = ...

    def ask_for_ownership(self, posx, posy):
        # return True / False
        pass

    def give_ownership(self, posx, posy):
        pass

    def deny_ownership(self, posx, posy):
        pass

    def check_messages(self):
        # check for messages from other players
        # making this function a generator might be a good idea
        # handle the message in the controller
        pass

    def connect(self, ip, port):
        # connect to a game
        # return the game it is connected to
        pass

    def diconnect(self):
        # cleanly disconnectand release all owned objects
        # if done well I believe the process is the same wether there are players still
        # connected or not
        pass

    def create(self):
        # create a game a make it available for others to connect
        # return the game
        # probably not the best file for this function
        pass
