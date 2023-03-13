from dataclasses import dataclass

from Model.Grass import Grass
from Model.House import House
from Model.Other_Rock import Other_Rock
from Model.Prefecture import Prefecture
from Model.Engineer_Post import Engineer_Post
from Model.Collapsed import Collapsed
from Model.Road import Road
from Model.Rock import Rock
from Model.Tree import Tree
from Model.Water import Water
from Model.Well import Well
from Model.Fountain import Fountain
from Model.Senate import Senate
from Model.Garden import Garden
from Model.Forum import Forum
from Model.Wheat_Farm import Wheat_Farm
from Model.Granary import Granary
from Model.Market import Market
from Model.Sign import Sign
from Model.New_House import New_House



@dataclass
class Building_Data:
    price: int
    des_init: int
    des_step: int
    des_step_size: int
    des_range: int


building_data = {House: Building_Data(0, 0, 0, 0, 0),
                 Prefecture: Building_Data(30, -2, 1, 1, 2),
                 Road: Building_Data(4, 0, 0, 0, 0),
                 Engineer_Post: Building_Data(30, 0, 1, 1, 1),
                 Collapsed: Building_Data(0, 0, 0, 0, 0),
                 Well: Building_Data(5, -1, 1, 2, 1),
                 Fountain: Building_Data(15, 0, 0, 0, 0),
                 Senate: Building_Data(400, 8, 2, -1, 8),
                 Garden: Building_Data(12, 3, 1, -1, 3),
                 Forum: Building_Data(75, 3, 2, -1, 2),
                 Wheat_Farm: Building_Data(40, -2, 1, 1, 2),
                 Granary: Building_Data(100, -4, 1, 2, 2),
                 Market: Building_Data(40, -2, 1, 1, 6),
                 Sign: Building_Data(0, 0, 0, 0, 0),
                 New_House: Building_Data(10, -3, 1, 1, 3),
                 Tree: Building_Data(0, 0, 0, 0, 0),
                 Water: Building_Data(0, 0, 0, 0, 0),
                 Rock: Building_Data(0, 0, 0, 0, 0),
                 Other_Rock: Building_Data(0, 0, 0, 0, 0),
                 Grass: Building_Data(0, 0, 0, 0, 0)
                 }
