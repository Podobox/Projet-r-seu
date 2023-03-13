from Model.Building import Building
from enum import Enum


class Sign_Type(Enum):
    Enter = 1
    Exit = 2


class Sign(Building):

    def __init__(self, tile):
        super().__init__(1, 1, tile, job_offered=0)
        self.type = None

    def __repr__(self):
        return f"Sign {self.type.name}"

    def set_type(self, type):
        self.type = type
