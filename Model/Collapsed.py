from Model.Building import Building


class Collapsed(Building):

    def __init__(self, tile, sizex=1, sizey=1):
        super().__init__(sizex, sizey, tile, 0)

    def __repr__(self):
        return "Collapsed"
