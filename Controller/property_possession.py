import Controller.Communication as com
from Model.Map import Map, MAP_DIM
class PropertyPossession:
    def __init__(self, comm, map):
        self.map = map
        self.comm = comm

    def modify_property(self, posx, posy):
        if self.comm.ask_for_ownership(posx, posy):

        self.map.grid[posx][posy].owner = com.ME
        print(self.map.grid[posx][posy].owner)
        print(f"Vous êtes maintenant propriétaire de la case ({posx}, {posy}).")
        # else:
            print("Accès refusé.")
    

    # def receive_property_request(self, tile, player):
    #     if self.is_owner(tile.posx, tile.posy, player):
    #         del self.owned_tiles[(tile.posx, tile.posy)]
    #         self.comm.deny_ownership(tile.posx, tile.posy, player)
    #         print(f"La case ({tile.posx}, {tile.posy}) a été libérée.")
    #     else:
    #         print("Vous n'êtes pas propriétaire de cette case.")
    
    # def count_properties(self, player):
    #     count = 0
    #     for tile in self.owned_tiles.values():
    #         if tile.player == player:
    #             count += 1
    #     return count
    
    
