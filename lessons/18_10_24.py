from random import randint
import pygame as pg
import copy

widht_in_cell = 100
height_in_cell = 100
cell_size = 5

size = width, height = widht_in_cell * cell_size + 1, height_in_cell * cell_size +1

tickspeed = 100

screen = pg.display.set_mode(size)
clock = pg.time.Clock()

next_stage = [[0 for i in range(widht_in_cell)] for j in range(height_in_cell)]
current_stage = [[randint(0, 1) for i in range(widht_in_cell)] for j in range(height_in_cell)]
# # Glaider
# current_stage[20][20] = 1
# current_stage[21][21] = 1
# current_stage[21][22] = 1
# current_stage[20][22] = 1
# current_stage[19][22] = 1
# # Ship
# current_stage[50][50] = 1
# current_stage[52][50] = 1
# current_stage[53][51] = 1
# current_stage[49][52] = 1
# current_stage[53][52] = 1
# current_stage[53][53] = 1
# current_stage[50][54] = 1
# current_stage[53][54] = 1
# current_stage[51][55] = 1
# current_stage[52][55] = 1
# current_stage[53][55] = 1


def paint_cell(position):
    y, x = position
    neighbours = 0
    y_range = [i for i in range(y-1, y+2)]
    x_range = [i for i in range(x-1, x+2)]
    for y_cell in y_range:
        for x_cell in x_range:
            if current_stage[y_cell][x_cell]:
                neighbours += 1
    if current_stage[y][x]:
        neighbours -= 1
        if neighbours in (2,3):
            return 1
        else:
            return 0
    else:
        if neighbours == 3:
            return 1
        else:
            return 0
        

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
            
    screen.fill(pg.Color('black'))
    #[pg.draw.line(screen, (150, 150, 150), (x, 0), (x, height)) for x in range(0, width, cell_size)]
    #[pg.draw.line(screen, (150, 150, 150), (0, y), (width, y)) for y in range(0, height, cell_size)]

    for x in range(1, widht_in_cell - 1):
        for y in range(1, height_in_cell - 1):
            if current_stage[y][x]:
                pg.draw.rect(screen, (255,255,255), (x * cell_size + 2, y * cell_size + 2, cell_size - 2, cell_size - 2))
            next_stage[y][x] = paint_cell((y, x))

    current_stage = copy.deepcopy(next_stage)
    clock.tick(tickspeed)
    pg.display.flip()