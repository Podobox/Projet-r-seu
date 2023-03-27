
from Controller.Communication import Communication
class Property_possession:
    comm = Communication()

    def __init__(self, player):
        self.player = player

    def is_owner(self, tile, player):
        return self.tile.player == self.player
    

    def modify_property(self, tile, player):
        if self.is_owner(tile, player):
            self.comm.give_ownership(tile, player)
            return True
            
        else:
            self.comm.ask_for_ownership(tile, player)
            if self.is_owner(tile, player):
                self.comm.give_ownership(tile, player)
            else:
                print("Access denied")

    def receive_property_request(self, tile, player):
        if not self.is_owner(tile, player):
            if self.comm.ask_for_ownership(id(tile), None):
                self.comm.give_ownership(id(tile), player)
            else:
                print("Access denied")