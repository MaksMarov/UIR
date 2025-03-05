import random
from cell import Cell
from params import PANIC_DEGREE
from enums import CellType

class Person:
    def __init__(self, start_position):
        self.position: Cell = None
        self.is_panicked = False
        self.survived = False
        self.is_dead = False
        self.move_to(start_position)
        
    def move(self, nearby_cells):
        self.check_safety()
        if self.survived or self.is_dead:
            return

        valid_cells = [
        cell for cell in nearby_cells
        if cell.cell_type in {CellType.FLOOR, CellType.EXIT} 
        and cell.is_accessible]

        if not valid_cells:
            return

        if self.is_panicked and random.random() > PANIC_DEGREE:
            new_position = random.choice(valid_cells)
        else:
            new_position = min(valid_cells, key=lambda n: n.distance_to_exit, default=None)
            
        if new_position:
            self.move_to(new_position)
            
    def move_to(self, new_position):
        if self.position:
            self.position.free_up()
        self.position = new_position
        
        if self.position.cell_type == CellType.EXIT:
            self.survived = True
            return
 
        self.position.occupy()

    def check_safety(self):
        if self.position.is_burning:
            self.is_dead = True
            return
        self.is_panicked = self.position.is_smoke