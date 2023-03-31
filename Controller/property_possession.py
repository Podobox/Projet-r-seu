from Controller.Communication import Communication
from Model.Tile import Tile

class PropertyPossession:
    def __init__(self, posx, posy, player):
        self.tile = Tile(posx=posx, posy=posy, type=None)
        self.owned_tiles = {}

    def is_owner(self, posx, posy, player):
        tile = self.owned_tiles.get((posx, posy))
        return tile is not None and tile.player == player

    def modify_property(self, posx, posy, player):
        if self.is_owner(posx, posy, player):
            print("Déjà propriétaire.")
        elif (posx, posy) in self.owned_tiles:
            print("Vous possédez déjà une case.")
        else:
            if Communication.ask_for_ownership(posx, posy):
                self.owned_tiles[(posx, posy)] = self.tile
                Communication.give_ownership(posx, posy, player)
                print(
                    f"Vous êtes maintenant propriétaire de la case ({posx}, {posy}).")
            else:
                print("Accès refusé.")
    
    def receive_property_request(self, tile, player):
        if self.is_owner(tile.posx, tile.posy, player):
            del self.owned_tiles[(tile.posx, tile.posy)]
            Communication.deny_ownership(tile.posx, tile.posy, player)
            print(f"La case ({tile.posx}, {tile.posy}) a été libérée.")
        else:
            print("Vous n'êtes pas propriétaire de cette case.")
    
    def count_properties(self, player):
        count = 0
        for tile in self.owned_tiles.values():
            if tile.player == player:
                count += 1
        return count
