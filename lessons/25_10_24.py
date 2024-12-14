from random import randint
from tkinter import Widget
import pygame as pg
import copy

widht_in_cell = 50
height_in_cell = 100
cell_size = 10

size = width, height = widht_in_cell * cell_size + 1, height_in_cell * cell_size +1

rocks_count = 500
bullshit_count = 0
winners_count = 0

death_rate = 90



time = 0

tickspeed = 10

screen = pg.display.set_mode(size)
clock = pg.time.Clock()

next_stage = [[0 for i in range(widht_in_cell)] for j in range(height_in_cell)]
current_stage = [[0 for i in range(widht_in_cell)] for j in range(height_in_cell)]
for _ in range(rocks_count):
    current_stage[randint(0, height_in_cell - 3)][randint(1, widht_in_cell - 1)] = 2
current_stage[height_in_cell - 2] = [randint(0, 1) for i in range(widht_in_cell)]
bullshit_count += sum(current_stage[height_in_cell - 2])


def new_stage(ref_stage):
    global bullshit_count, winners_count
    for x in range(1, widht_in_cell - 1):
        for y in range(1, height_in_cell - 1):
            if ref_stage[y][x] == 1:
                if y == 1:
                    ref_stage[y][x] = 0
                    winners_count += 1
                elif ref_stage[y - 1][x] == 0:
                    ref_stage[y][x] = 0
                    ref_stage[y - 1][x] = 1
                elif ref_stage[y][x - 1] == 0 or ref_stage[y][x + 1] == 0:
                    if randint(0,1):    
                        if ref_stage[y][x - 1] == 0:
                            ref_stage[y][x] = 0
                            ref_stage[y][x - 1] = 1
                        else:
                            ref_stage[y][x] = 0
                            ref_stage[y][x + 1] = 1
                    else:
                        if ref_stage[y][x + 1] == 0:
                            ref_stage[y][x] = 0
                            ref_stage[y][x + 1] = 1
                        else:
                            ref_stage[y][x] = 0
                            ref_stage[y][x - 1] = 1
                elif 1 in [ref_stage[y - 1][x], ref_stage[y][x-1], ref_stage[y][x+1]]:
                    if randint(0, 100) <= death_rate:
                        ref_stage[y][x] = 3
                

    if time % 10 == 0:
        current_stage[height_in_cell - 2] = [randint(0, 1) for i in range(widht_in_cell)]
        bullshit_count += sum(current_stage[height_in_cell - 2])
    return ref_stage


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            print(bullshit_count, winners_count, winners_count / bullshit_count)
            quit()
            
    screen.fill(pg.Color('white'))
    [pg.draw.line(screen, (150, 150, 150), (x, 0), (x, height)) for x in range(0, width, cell_size)]
    [pg.draw.line(screen, (150, 150, 150), (0, y), (width, y)) for y in range(0, height, cell_size)]
    time += 1
    for x in range(1, widht_in_cell - 1):
        for y in range(1, height_in_cell - 1):
            if current_stage[y][x] == 2:
                pg.draw.rect(screen, pg.Color("gray"), (x * cell_size + 1, y * cell_size + 1, cell_size - 1, cell_size - 1))
            if current_stage[y][x] == 1:
                pg.draw.rect(screen, pg.Color("red"), (x * cell_size + 1, y * cell_size + 1, cell_size - 1, cell_size - 1))
            if current_stage[y][x] == 3:
                pg.draw.rect(screen, pg.Color("black"), (x * cell_size + 1, y * cell_size + 1, cell_size - 1, cell_size - 1))
 
    current_stage = new_stage(current_stage)
    clock.tick(tickspeed)
    pg.display.flip()