from Lab3.crossroad.enums import CellType, LightSignal, CellDirection

# клетка (просто клетка, что еще нужно?)
class Cell():
    def __init__(self, cell_type):
        self.cell_type = cell_type
        
# обочина (клетка заполнитель, по ней нельзя двигаться, определяет края дороги)
class Roadside(Cell):
    def __init__(self, cell_type):
        super().__init__(cell_type)
  
# дорога (позволяет объектам находиться внутри нее)
class Road(Cell):
    def __init__(self, cell_type):
        super().__init__(cell_type)
        self.contained_obj = None
        
    def get_availability(self):
        return not self.contained_obj

# однонаправленная дорога (поддерживет движение в единственном направлении и престроение)
class UniDirectionalRoad(Road):
    def __init__(self, cell_type):
        super().__init__(cell_type)
        self.direction = CellDirection.NONE
        self.straight_path = None
        # ссылки на клетки для перестроения
        self.right_lane = None
        self.left_lane = None
        
# разнонаправленная дорога (поддерживает движение в любом направлении)
class MultiDirectionalRoad(Road):
    def __init__(self, cell_type):
        super().__init__(cell_type)
        self.direction_forks = [DirectionalFork(CellDirection(direction)) for direction in range(1, 5)]
        
    def get_fork_by_direction(self, direction):
        fork = next((fork for fork in self.direction_forks if fork.direction == direction), None)
        if fork:
            return fork
        else: 
            print(f"Error. Fork for this direction is not exist. Direction = {direction}, Self = {self}")
     
# хранит набор ссылок привязанный к направлению
class DirectionalFork():
    def __init__(self, direction):
        self.direction = direction
        self.straight_path = None
        self.right_path = None
        self.left_path = None
        self.back_way = None
        
    def get_straight_or_any_path(self):
        path = self.straight_path if self.straight_path else self.right_path if self.right_path else self.left_path if self.left_path else self.back_way if self.back_way else None
        if path:
            return path
        else:
            print(f"Error. Straight path is not exist and any path not found. Self = {self} Straight = {self.straight_path} Right = {self.right_path} Left = {self.left_path} Backway = {self.back_way} Dirrection = {self.direction}")

# светофор (позволяет контолировать движение внутри самого себя)
class TrafficLight(UniDirectionalRoad):
    def __init__(self, cell_type):
        super().__init__(cell_type)
        self.light_signal = LightSignal.TURNED_OFF
        
    def get_availability(self):
        return not self.contained_obj and self.light_signal in (LightSignal.GREEN, LightSignal.TURNED_OFF)
    

class RoadZone():
    def __init__(self):
        self.cells = []
        
    def add_cell(self, cell):
        if cell and isinstance(cell, Road):
            self.cells.append(cell)
        else:
            print(f"Error. Cell was null or wrong type. Cell={cell}")
            
    def add_cells(self, cells):
        for cell in cells:
            self.add_cell(cell)
            
    def get_obj_count(self):
        obj_count = sum(1 for cell in self.cells if cell.contained_obj)
        return obj_count
    
    def is_empty(self):
        return not self.get_obj_count() > 0
    
    def get_capacity(self):
        return len(self.cells)
    
    def get_fullness_ratio(self):
        if self.get_capacity():
            return self.get_obj_count() / self.get_capacity()
        else:
            return 0 
    

class ZoneContainer():
    def __init__(self):
        self.ns_zone = RoadZone()
        self.ew_zone = RoadZone()
        self.crossroad_zone = RoadZone()
        
# фабрика клеток(создает клетки в зависимости от их типа (типа шарим за фабричные методы, you know(еще и за статические методы, you know(а также за match-case, you know(кст, этот код не запустится на версии питона ниже 3.10)))))
class CellFactory:
    @staticmethod
    def create_cell(cell_type):
        match cell_type:
            case CellType.ROADSIDE:
                return Roadside(cell_type)
            case CellType.UD_ROAD:
                return UniDirectionalRoad(cell_type)
            case CellType.TRAFFIC_LIGHT:
                return TrafficLight(cell_type)
            case CellType.MD_ROAD:
                return MultiDirectionalRoad(cell_type)
            case _:
                return Cell(CellType.EMPTY)