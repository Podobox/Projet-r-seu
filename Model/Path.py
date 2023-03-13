# from Model.Map import Map
from Model.Road import Road
# from Model.Map import MAP_DIM
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

MAP_DIM = 30

def create_path_matrix(map):
    path_matrix = [[10000 for x in range(MAP_DIM)] for y in range(MAP_DIM)]
    for x in range(MAP_DIM):
        for y in range(MAP_DIM):
            if map.is_type(x, y, Road):
                path_matrix[x][y] = 1
            elif map.grid[x][y].building is None:
                path_matrix[x][y] = 1000
    return path_matrix
