from grid import Grid
from enums import CellType
from data_tool import import_map

class Simulation:
    def __init__(self, width = 40, height = 40, load_map = True):
        if load_map:
            self.grid = import_map()
        else:
            self.grid = Grid(width, height)
            self.grid.generate_structured_grid()
        self.grid.prepare()
        self.running = True
        self.timer = 0

    def update(self):
        if not self.running:
            return False
        
        if self.grid.complete():
            return True

        self.grid.update()
        self.timer+=1
    
    def toggle_pause(self):
        self.running = not self.running


