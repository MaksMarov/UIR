from enum import Enum

class CellType(Enum):
    FILLER = 0
    EXIT = 1
    FLOOR = 2
    WALL = 3