import pygame
import sys
from grid import Grid
from enums import CellType
from lab5.cell import create_cell
from data_tool import save_to_csv, import_map

if len(sys.argv) >= 3:
    grid_width = int(sys.argv[1])
    grid_height = int(sys.argv[2])
else:
    grid_width, grid_height = 190, 100

CELL_SIZE = 10
WIDTH, HEIGHT = grid_width * CELL_SIZE, grid_height * CELL_SIZE

grid = Grid(grid_width, grid_height)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

selected_type = CellType.FLOOR
running = True
show_distances = False
distance_calculated = False

def toggle_distance_display():
    global show_distances
    show_distances = not show_distances

def flood_fill(x, y, target_type, replacement_type):
    if target_type == replacement_type:
        return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if 0 <= cx < grid.width and 0 <= cy < grid.height and grid.get_cell(cx, cy).cell_type == target_type:
            grid.set_cell(cx, cy, replacement_type)
            stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])

def draw_grid():
    screen.fill((0, 0, 0))
    colors = {
        CellType.FLOOR: (194, 169, 126),
        CellType.WALL: (0, 0, 0),       
        CellType.EXIT: (255, 0, 0),     
        CellType.FILLER: (46, 204, 113) 
    }
    
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.get_cell(x, y)
            color = colors.get(cell.cell_type, (50, 50, 50))
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (200, 200, 200), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            
            if show_distances and distance_calculated and hasattr(cell, 'distance_to_exit') and cell.distance_to_exit >= 0:
                font = pygame.font.Font(None, 10)
                text = font.render(str(cell.distance_to_exit), True, (255, 255, 255))
                screen.blit(text, (x * CELL_SIZE, y * CELL_SIZE))

grid.generate_structured_grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                selected_type = CellType.FILLER
            elif event.key == pygame.K_1:
                selected_type = CellType.WALL
            elif event.key == pygame.K_2:
                selected_type = CellType.FLOOR
            elif event.key == pygame.K_3:
                selected_type = CellType.EXIT
            elif event.key == pygame.K_s:
                save_to_csv(grid)
            elif event.key == pygame.K_l:
                grid = import_map()
                show_distances = False
                distance_calculated = False
            elif event.key == pygame.K_SPACE:
                grid.compute_wavefront()
                show_distances = True
                distance_calculated = True
            elif event.key == pygame.K_d:
                toggle_distance_display()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
            if event.button == 1:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    flood_fill(x, y, grid.get_cell(x, y).cell_type, selected_type)
                else:
                    grid.set_cell(x, y, selected_type)
            elif event.button == 3:
                grid.set_cell(x, y, CellType.FLOOR)
    
    draw_grid()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
