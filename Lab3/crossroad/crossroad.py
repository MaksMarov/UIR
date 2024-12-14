from Lab3.crossroad.cell import Cell, Roadside, UniDirectionalRoad, MultiDirectionalRoad, TrafficLight, CellFactory, Road, RoadZone, ZoneContainer
from Lab3.crossroad.enums import CellDirection, CrossroadType, CellType

from copy import deepcopy

# класс перекрестка ()
class Crossroad():
    def __init__(self, type, roads_length):
        self.type = type
        self.road_length = roads_length
        self.size = roads_length + type.value + 1
        self.grid = self.create_grid()

    # Создание четверти матрицы(птм что полностью генерить сразу впадлу и так правильнее по итогу)
    def generate_quarter(self):
        grid = [[CellFactory.create_cell(CellType.EMPTY) for _ in range(self.size)] for _ in range(self.size)]

        for i in range(self.road_length+1):
            grid[i][self.road_length] = CellFactory.create_cell(CellType.ROADSIDE)
            for k in range(self.type.value):
                if i == self.road_length:
                    grid[i][self.road_length + k + 1] = CellFactory.create_cell(CellType.TRAFFIC_LIGHT)
                else:
                    grid[i][self.road_length + k + 1] = CellFactory.create_cell(CellType.UD_ROAD)
                grid[i][self.road_length + k + 1].direction = CellDirection.NORTH

        for j in range(self.road_length+1):
            grid[self.road_length][j] = CellFactory.create_cell(CellType.ROADSIDE)
            for k in range(self.type.value):
                grid[self.road_length + k + 1][j] = CellFactory.create_cell(CellType.UD_ROAD)
                grid[self.road_length + k + 1][j].direction = CellDirection.WEST
    
        for i in range(self.type.value):
            for j in range(self.type.value):
                grid[self.road_length + 1 + i][self.road_length + 1 + j] = CellFactory.create_cell(CellType.MD_ROAD)

        return grid

    # Простой поворот матрицы
    def matrix_rotate(self, matrix):
        return [list(reversed(col)) for col in zip(*matrix)]

    # Поворот матрицы с учетом поворота их внутренних направлений 
    def rotate_quarter(self, matrix, angle):
        rotations = (angle // 90) % 4
        rotated_matrix = matrix
        for _ in range(rotations):
            rotated_matrix = self.matrix_rotate(rotated_matrix)
            
        for row in rotated_matrix:
            for cell in row:
                if isinstance(cell, UniDirectionalRoad) and cell.direction != CellDirection.NONE:
                    cell.direction = CellDirection((cell.direction.value % 4) + rotations)
                
        return rotated_matrix
    
    # Собираем все четверти в одну
    def combine_quarters(self, quarter11, quarter12, quarter21, quarter22):
        grid = [[0] * self.size * 2 for _ in range(self.size * 2)]

        for i in range(self.size):
            for j in range(self.size):
                grid[i][j] = quarter11[i][j]
                grid[i][j + self.size] = quarter12[i][j]
                grid[i + self.size][j] = quarter21[i][j]
                grid[i + self.size][j + self.size] = quarter22[i][j]
    
        return grid
    
    # Задаем прямые пути и перестроения для четверти
    def set_communications(self, quarter):
        central_lane = (self.type.value // 2) + 1
        central_lane_index = self.road_length + central_lane
        
        for i in range(self.road_length + 1):
            self.try_set_straight_path(quarter, i, central_lane_index)
            
            for offset in (-1, 1):
                neighbor_index = central_lane_index + offset
                if self.is_valid_lane(quarter, i, neighbor_index):
                    if isinstance(quarter[i][neighbor_index], UniDirectionalRoad):
                        if not isinstance(quarter[i][neighbor_index], TrafficLight):
                            if offset == -1:
                                quarter[i][central_lane_index].right_lane = quarter[i][neighbor_index]
                                quarter[i][neighbor_index].left_lane = quarter[i][central_lane_index]
                            elif offset == 1:
                                quarter[i][central_lane_index].left_lane = quarter[i][neighbor_index]
                                quarter[i][neighbor_index].right_lane = quarter[i][central_lane_index]
                            else:
                                print(f"Error. Incorect value. Offset = {offset}")
                        self.try_set_straight_path(quarter, i, neighbor_index)
        
        for i in range(self.road_length, -1, -1):
            self.try_set_straight_path_hor(quarter, central_lane_index, i)
            
            for offset in (-1, 1):
                neighbor_index = central_lane_index + offset
                if self.is_valid_lane(quarter, neighbor_index, i):
                    if isinstance(quarter[neighbor_index][i], UniDirectionalRoad):
                        self.try_set_straight_path_hor(quarter, neighbor_index, i)

        return quarter

    # Пытаемся установить следующий прямой элемент 
    def try_set_straight_path(self, grid, index, lane):
        if index + 1 < len(grid) and isinstance(grid[index + 1][lane], UniDirectionalRoad):
            grid[index][lane].straight_path = grid[index + 1][lane]
            
    # Пытаемся установить следующий прямой элемент но с другим индексом(внутри строки)
    def try_set_straight_path_hor(self, grid, lane, index):
        if index - 1 >= 0 and isinstance(grid[lane][index - 1], UniDirectionalRoad):
            grid[lane][index].straight_path = grid[lane][index - 1]

    # Проверяем индексы
    def is_valid_lane(self, grid, row, col):
        return 0 <= row < len(grid) and 0 <= col < len(grid[row])

    # Устанавливаем пути в центре перекрестка
    def set_crossroad_paths(self, grid):
        
        def create_right_path(road_index, lane_index, direction):
            grid[road_index + 1][lane_index].get_fork_by_direction(direction).right_path = grid[road_index + 1][lane_index - 1]

        def create_straight_path(road_index, lane_index, direction):
            i = 1
            while not isinstance(grid[road_index + i][lane_index], UniDirectionalRoad):
                grid[road_index + i][lane_index].get_fork_by_direction(direction).straight_path = grid[road_index + i + 1][lane_index]
                i += 1
            
        def create_left_path(road_index, lane_index, direction):
            new_road_index = 0
            for i in range(1, self.type.value + 1):
                grid[road_index + i][lane_index].get_fork_by_direction(direction).left_path = grid[road_index + i + 1][lane_index]
                new_road_index = road_index + i + 1
            grid[new_road_index][lane_index].get_fork_by_direction(direction).left_path = grid[new_road_index][lane_index + 1]
            j = 1
            while not isinstance(grid[new_road_index][lane_index + j], UniDirectionalRoad):
                grid[new_road_index][lane_index + j].get_fork_by_direction(direction).left_path = grid[new_road_index][lane_index + j + 1]
                j += 1
        
        def create_back_way(road_index, lane_index, direction):
            grid[road_index + 1][lane_index].get_fork_by_direction(direction).back_way = grid[road_index + 1][lane_index + 1]
            grid[road_index + 1][lane_index + 1].get_fork_by_direction(direction).back_way = grid[road_index][lane_index + 1]

        for _ in range(4):
            for lane in range(1, self.type.value + 1):
                road_index = self.road_length
                lane_index = self.road_length + lane
                _cell_dir = grid[road_index][lane_index].direction
                grid[road_index][lane_index].straight_path = grid[road_index + 1][lane_index]
                
                if self.type.value == 1:
                    create_right_path(self.road_length, lane_index, _cell_dir)
                    create_straight_path(self.road_length, lane_index, _cell_dir)
                    create_left_path(self.road_length, lane_index, _cell_dir)
                    create_back_way(self.road_length, lane_index, _cell_dir)
                elif lane == 1:
                    create_right_path(self.road_length, lane_index, _cell_dir)
                elif lane == 2:
                    if self.type.value > 2:
                        create_straight_path(self.road_length, lane_index, _cell_dir)
                    else:
                        create_straight_path(self.road_length, lane_index, _cell_dir)
                        create_left_path(self.road_length, lane_index, _cell_dir)
                        create_back_way(self.road_length, lane_index, _cell_dir)
                else:
                    create_straight_path(self.road_length, lane_index, _cell_dir)
                    create_left_path(self.road_length, lane_index, _cell_dir)
                    create_back_way(self.road_length, lane_index, _cell_dir)
            
            grid = self.matrix_rotate(grid)
            
        return grid       

    # Генерация полной матрицы перекрестка
    def create_grid(self):        
        quarter = self.generate_quarter()

        _11 = self.set_communications(deepcopy(quarter))
        _12 = self.rotate_quarter(self.set_communications(deepcopy(quarter)), 90)
        _21 = self.rotate_quarter(self.set_communications(deepcopy(quarter)), 270)
        _22 = self.rotate_quarter(self.set_communications(deepcopy(quarter)), 180)
    
        grid = self.combine_quarters(_11, _12, _21, _22)
        
        return self.set_crossroad_paths(grid)
    
    # Получаем список всех светофоров
    def get_tlights(self):
        tlights = []
        for row in self.grid:
            for elem in row:
                if isinstance(elem, TrafficLight):
                    tlights.append(elem)
        return tlights
                    
    # Получаем начальные и конечные точки дорог
    def get_start_end_points(self):
        s_points = []
        e_points = []
        
        for i in range(1, self.type.value + 1):
            s_points.append(self.grid[0][self.road_length + i])
            e_points.append(self.grid[0][self.road_length + self.type.value + i])
            s_points.append(self.grid[len(self.grid) - 1][self.road_length + self.type.value + i])
            e_points.append(self.grid[len(self.grid) - 1][self.road_length + i])
            s_points.append(self.grid[self.road_length + self.type.value + i][0])
            e_points.append(self.grid[self.road_length + i][0])
            s_points.append(self.grid[self.road_length + i][len(self.grid) - 1])
            e_points.append(self.grid[self.road_length + self.type.value + i][len(self.grid) - 1])
            
        return [s_points, e_points]

    def get_zones(self):
        zones = ZoneContainer()
        grid = self.grid
        i, j = self.road_length + 1, self.road_length + self.type.value + 1
        for _ in range(4):
            sub_grid = [row[:j] for row in grid[:i]]
            for row in sub_grid:
                for cell in row:
                    if isinstance(cell, UniDirectionalRoad):
                        if cell.direction in (CellDirection.NORTH, CellDirection.SOUTH):
                            zones.ns_zone.add_cell(cell)
                        if cell.direction in (CellDirection.EAST, CellDirection.WEST):
                            zones.ew_zone.add_cell(cell)
                    elif isinstance(cell, MultiDirectionalRoad):
                        zones.crossroad_zone.add_cell(cell)
            grid = self.matrix_rotate(grid)   
        for row in self.grid:
                for cell in row:
                    if isinstance(cell, MultiDirectionalRoad):
                        zones.crossroad_zone.add_cell(cell)
        return zones