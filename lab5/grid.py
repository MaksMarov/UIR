from collections import deque
import random
from typing import List
from enums import CellType
from cell import Cell, create_cell
from person import Person
from params import FIRE_PROBABILITIES, FIRE_ACTIVITY, SMOKE_PROBABILITIES, SMOKE_ACTIVITY, PEOPLE_COUNT, RANDOM_SEED


class Grid:
    def __init__(self, width: int, height: int, seed = RANDOM_SEED):
        self.width = width
        self.height = height
        self.grid = [[create_cell(CellType.FILLER, i, j) for i in range(width)] for j in range(height)]
        self.burning_cells = []
        self.smoke_cells = []
        self.people : List[Person] = []
        self.dead_people : List[Person] = []
        self.survived_people : List[Person] = []
        self.local_random = random.Random(seed)
        
    def prepare(self):
        self.compute_wavefront()
        self.generate_people(PEOPLE_COUNT)
        self.ignite_random_floor_cell()
        self.update_burning_cells()
        self.update_smoke_cells()
    
    def set_cell(self, x: int, y: int, cell_type: CellType):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = create_cell(cell_type, x, y)
        else:
            raise ValueError(f"Coordinates ({x}, {y}) are out of grid bounds")
    
    def get_cell(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def get_neighbors(self, cell: Cell, diagonal=False):
        x = cell.x
        y = cell.y
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if diagonal:
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append(self.grid[ny][nx])
        
        return neighbors

    def compute_wavefront(self):
        queue = deque()
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.cell_type == CellType.EXIT:
                    cell.distance_to_exit = 0
                    queue.append(cell)
                else:
                    cell.distance_to_exit = -1
        
        while queue:
            cell = queue.popleft()
            for neighbor in self.get_neighbors(cell):
                if neighbor.cell_type in {CellType.FLOOR, CellType.EXIT} and not neighbor.is_burning and (neighbor.distance_to_exit == -1 or neighbor.distance_to_exit > cell.distance_to_exit + 1):
                    neighbor.distance_to_exit = cell.distance_to_exit + 1
                    queue.append(neighbor)
    
    def generate_structured_grid(self, exit_count=3):
        for y in range(self.height):
            for x in range(self.width):
                self.set_cell(x, y, CellType.WALL)
        
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.set_cell(x, y, CellType.FLOOR)
        
        for _ in range(exit_count):
            x, y = random.choice([(0, random.randint(1, self.height - 2)),
                                  (self.width - 1, random.randint(1, self.height - 2)),
                                  (random.randint(1, self.width - 2), 0),
                                  (random.randint(1, self.width - 2), self.height - 1)])
            self.set_cell(x, y, CellType.EXIT)

    def spread_fire(self):
        for cell in self.burning_cells:
            for neighbor in self.get_neighbors(cell):
                if not neighbor.is_burning and neighbor.cell_type:
                    fire_probability = FIRE_PROBABILITIES[neighbor.cell_type.value] * FIRE_ACTIVITY
                    if random.random() < fire_probability:

                        neighbor.ignite()
                        self.burning_cells.append(neighbor)

    def spread_smoke(self):
        for cell in self.smoke_cells:
            for neighbor in self.get_neighbors(cell, diagonal=True):
                if not neighbor.is_smoke and neighbor.cell_type == CellType.FLOOR:
                    smoke_probability = SMOKE_PROBABILITIES[neighbor.cell_type.value] * SMOKE_ACTIVITY
                    if random.random() < smoke_probability:
                        neighbor.smoke()
                        self.smoke_cells.append(neighbor)

        for cell in self.burning_cells:
            for neighbor in self.get_neighbors(cell):
                if not neighbor.is_smoke and neighbor.cell_type == CellType.FLOOR:
                    neighbor.smoke()
                    self.smoke_cells.append(neighbor)

    def update_burning_cells(self):
        self.burning_cells = [cell for row in self.grid for cell in row if cell.is_burning]

    def update_smoke_cells(self):
        self.smoke_cells = [cell for row in self.grid for cell in row if cell.is_smoke]

    def ignite_random_floor_cell(self):
        floor_cells = [cell for row in self.grid for cell in row if cell.cell_type == CellType.FLOOR]
        if floor_cells:
            self.local_random.choice(floor_cells).ignite()
            
    def generate_people(self, count):
        floor_cells = [cell for row in self.grid for cell in row if cell.cell_type == CellType.FLOOR and cell.is_accessible]
        
        if len(floor_cells) < count:
            raise ValueError("Not enough available floor cells to place all people.")

        self.local_random.shuffle(floor_cells)

        for i in range(count):
            person = Person(floor_cells[i])
            self.people.append(person)
            
        print(f"People was generated {len(self.people)}")
            
    def update(self):
        self.spread_fire()
        self.spread_smoke()
        self.compute_wavefront()
        
        new_people = []
        for person in self.people:
            if person.is_dead:
                self.dead_people.append(person)
            elif person.survived:
                self.survived_people.append(person)
            else:
                person.move(self.get_neighbors(person.position))
                new_people.append(person)
            
        self.people = new_people

    def complete(self):
        return len(self.people) < 1