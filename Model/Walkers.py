import random
import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from Model.Road import Road
from Model.Path import create_path_matrix
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Action(Enum):
    NONE = -1
    BUILD_HOUSE = -2
    DESTROY_SELF = -3


def will_pass_middle(x, delta_x):
    return (x - int(x) - 0.5) * ((x + delta_x) - int(x) - 0.5) < 0


class Walkers:
    def __init__(self, map, spawn_road):
        self.map = map
        self.speed = 640 / 365 / 24 / 60  # tiles per minutes
        self.spawn_road = spawn_road
        self.posx = spawn_road.tile.posx + 0.5
        self.posy = spawn_road.tile.posy + 0.5
        self.date_last_frame = None
        self.direction = None
        self.display_action_counter = 1
        self.destination = None  # tuple(x, y)

    def __str__(self):
        string = self.__repr__()
        string += f"\n\t({self.posx}, {self.posy})"
        if self.destination is None:
            string += "\n\tNo destination"
        else:
            string += f"\n\tDestination ({self.destination[0]}, {self.destination[1]})"
        if self.direction is None:
            string += "\n\tNo Direction"
        else:
            string += f"\n\tGoing {self.direction.name}"
        return string

    def roll_action(self):
        self.display_action_counter += 0.15
        if self.display_action_counter > 12:
            self.display_action_counter = 1
        if self.display_action_counter >= 10:
            return str(int(self.display_action_counter))
        else:
            return "0" + str(int(self.display_action_counter))

    def is_at_spawn_road(self):
        return int(self.posx) == self.spawn_road.tile.posx and \
            int(self.posy) == self.spawn_road.tile.posy

    def create_path(self, new_pos):
        x = new_pos[0]
        y = new_pos[1]
        self.grid = Grid(matrix=create_path_matrix(self.map))
        self.start = self.grid.node(int(self.posy), int(self.posx))
        self.end = self.grid.node(y, x)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        self.path_index = 0
        self.path, runs = finder.find_path(self.start, self.end, self.grid)

    # return True if middle was passed, False else
    def move(self, dist):
        middle_passed = False
        if self.direction == Direction.LEFT:
            self.posx = self.posx
            if will_pass_middle(self.posy, -dist):
                middle_passed = True
            self.posy = self.posy - dist
        elif self.direction == Direction.RIGHT:
            self.posx = self.posx
            if will_pass_middle(self.posy, dist):
                middle_passed = True
            self.posy = self.posy + dist
        elif self.direction == Direction.DOWN:
            if will_pass_middle(self.posx, dist):
                middle_passed = True
            self.posx = self.posx + dist
            self.posy = self.posy
        elif self.direction == Direction.UP:
            if will_pass_middle(self.posx, -dist):
                middle_passed = True
            self.posx = self.posx - dist
            self.posy = self.posy
        return middle_passed

    def compute_dist(self, date):
        return (date - self.date_last_frame).total_seconds() / 60 * self.speed

    def find_direction(self, x, y):
        if x == int(self.posx) - 1 and y == int(self.posy):
            self.direction = Direction.UP
        elif x == int(self.posx) + 1 and y == int(self.posy):
            self.direction = Direction.DOWN
        elif x == int(self.posx) and y == int(self.posy) - 1:
            self.direction = Direction.LEFT
        elif x == int(self.posx) and y == int(self.posy) + 1:
            self.direction = Direction.RIGHT
        else:
            print(f"({self.posx}, {self.posy}) -> ({x}, {y})\n")
            print(self.path)
            assert False, "wrong direction"

    # reurn True if at destination, else False
    def walk_to_destination(self, date, action):
        # print(f"({self.posx}, {self.posy})")
        if self.date_last_frame is None:
            self.date_last_frame = date
            return False

        if self.destination is None:
            self.find_destination(action)
            if (int(self.posx), int(self.posy)) == self.destination:
                # destination is our position
                if action:
                    self.action_post()
                self.destination = None
            self.date_last_frame = date
            return False

        if self.direction is None:
            self.create_path(self.destination)

            if len(self.path) == 0:
                # No path
                return False
            if len(self.path) == 1:
                # Arrived
                return True

            self.find_direction(self.path[1][1], self.path[1][0])

        dist = self.compute_dist(date)

        middle_passed = self.move(dist)
        if middle_passed:
            self.posx = int(self.posx) + 0.5
            self.posy = int(self.posy) + 0.5
            self.direction = None
            if (int(self.posx), int(self.posy)) == self.destination:
                self.date_last_frame = date
                self.destination = None
                return True
            else:
                self.create_path(self.destination)
                self.find_direction(self.path[1][1], self.path[1][0])

        self.date_last_frame = date
        return False

    def find_destination(self):
        assert False, "virtual function call"
