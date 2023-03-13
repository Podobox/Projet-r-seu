from Model.Walkers import Walkers
from enum import Enum


class Destination_Walkers(Walkers):
    def __init__(self, map, spawn_road):
        super().__init__(map, spawn_road)

    def __repr__(self):
        return "Destination_Walker"

    def __str__(self):
        string = super().__str__()
        string += f"\n\tDestination: {str(self.destination)}"
        return string

    def walk(self, date):
        if self.walk_to_destination(date):
            return self.action_post()

    def find_destination(self):
        assert False, "virtual function call"
