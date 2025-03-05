from grid import Grid
from enums import CellType
import pygame
import pygame.font

class Renderer:
    def __init__(self, grid, cell_size=10):
        self.grid = grid
        self.cell_size = cell_size
        self.width = grid.width * cell_size
        self.height = grid.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fire Simulation")
        self.font = pygame.font.SysFont(None, self.cell_size)
    
    def draw_grid(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                color = self.get_cell_color(cell)
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
    
    def get_cell_color(self, cell):
        if cell.is_burning:
            return (255, 140, 0)
        if cell.is_smoke:
            return (100, 100, 100, 100)
        if cell.cell_type == CellType.FLOOR:
            return (194, 169, 126)
        if cell.cell_type == CellType.WALL:
            return (50, 50, 50)
        if cell.cell_type == CellType.EXIT:
            return (0, 255, 0)
        return (46, 204, 113)
    
    def draw_fire_layer(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell.is_burning:
                    pygame.draw.rect(self.screen, (255, 140, 0), (x * self.cell_size + 4, y * self.cell_size + 4, self.cell_size - 8, self.cell_size - 8))
    
    def draw_smoke_layer(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell.is_smoke:
                    smoke_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    smoke_surface.fill((200, 200, 200, 100))
                    self.screen.blit(smoke_surface, (x * self.cell_size, y * self.cell_size))
    
    def draw_people(self, people):
        for person in people:
            cell = person.position
            if not cell:
                continue

            x, y = cell.x, cell.y

            color = (0, 110, 0) if not person.is_panicked else (128, 0, 128)
            pygame.draw.circle(
                self.screen, color,
                (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                self.cell_size // 3
            )
            
    def draw_distances(self):
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell.distance_to_exit >= 0:
                    text_surface = self.font.render(str(cell.distance_to_exit), True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(x * self.cell_size + self.cell_size // 2, 
                                                               y * self.cell_size + self.cell_size // 2))
                    self.screen.blit(text_surface, text_rect)
    
    def render(self, people=[]):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_fire_layer()
        self.draw_people(people)
        self.draw_smoke_layer()
        #self.draw_distances()
        pygame.display.flip()
