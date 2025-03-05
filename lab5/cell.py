import math
from enums import CellType

class Cell:
    def __init__(self, cell_type: CellType, x: int, y: int):
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.is_burning = False
        self.is_smoke = False

    def smoke(self):
        pass

    def ignite(self):
        pass
    
    def occupy(self):
        pass
        
    def free_up(self):
        pass

    def is_accessible(self) -> bool:
        return False


class FloorCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(CellType.FLOOR, x, y)
        self.occupied = False
        self.distance_to_exit = -1
        
    def smoke(self):
        self.is_smoke = True

    def ignite(self):
        self.is_burning = True
        
    def occupy(self):
        self.occupied = True
        
    def free_up(self):
        self.occupied = False

    def is_accessible(self) -> bool:
        return not self.is_burning and not self.occupied


class WallCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(CellType.WALL, x, y)
        
    def ignite(self):
        self.is_burning = True


class ExitCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(CellType.EXIT, x, y)
        self.occupied = False
        self.distance_to_exit = 0

    def is_accessible(self) -> bool:
        return True


class FillerCell(Cell):
    def __init__(self, x: int, y: int):
        super().__init__(CellType.FILLER, x, y)
       
    def smoke(self):
        self.is_smoke = True


def create_cell(cell_type: CellType, x: int, y: int) -> Cell:
    match cell_type:
        case CellType.FILLER:
            return FillerCell(x, y)
        case CellType.FLOOR:
            return FloorCell(x, y)
        case CellType.WALL:
            return WallCell(x, y)
        case CellType.EXIT:
            return ExitCell(x, y)
        case _:
            raise ValueError(f"Unknown cell type: {cell_type} for x: {x} y: {y}")