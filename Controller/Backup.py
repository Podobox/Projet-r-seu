from Model.Game import Game
import pickle
from os import mkdir, path


class Backup():
    def __init__(self, name_save):
        self.dir = "Save/"
        self.name_save = name_save

    # save a game
    def save(self, game):
        backup_path = self.dir + self.name_save
        if not path.exists(self.dir):
            mkdir(self.dir)
        backup_file = open(backup_path, "wb")

        pickle.dump(game, backup_file)

        backup_file.close()

    # return the game if found else None
    def load(self, backup_name):
        backup_path = self.dir + backup_name
        if not path.exists(backup_path):
            return None
        backup_file = open(backup_path, "rb")

        game = pickle.load(backup_file)

        backup_file.close()
        return game
