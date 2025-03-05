from tkinter import END
from Lab3.crossroad.car import Car, CarController
from Lab3.crossroad.crossroad import Crossroad
from Lab3.crossroad.traffic_light_controller import TrafficLightController
from Lab3.crossroad.enums import CrossroadType, TrafficLightControllerState, CellType, LightSignal, GenerationPriority
from Lab3.crossroad.cell import Cell, Road, Roadside, TrafficLight
import pygame as pg
from Lab3.crossroad.data import SimReport, GlobalData


class Game():
    def __init__(self, crossroad_type = CrossroadType.THREE_LANE, road_lenght = 15, tl_manager_type = TrafficLightControllerState.ADAPTIVE):
        self.crossroad_type = crossroad_type
        self.road_lenght = road_lenght
        self.tl_manager_type = tl_manager_type
        self.cpg = int(self.crossroad_type.value * 4 * 2 / 3)
        self.crossroad = Crossroad(self.crossroad_type, self.road_lenght)
        self.tl_controller = TrafficLightController(self.tl_manager_type, self.crossroad.get_tlights(), self.crossroad.get_zones())
        self.car_controller = CarController(points=self.crossroad.get_start_end_points(), cars_per_generation=self.cpg, gen_priority=GenerationPriority.EW, start_delay_tick=40, end_delay_tick=3, generations_count=30)
        self.widht_in_cell = len(self.crossroad.grid)
        self.height_in_cell = len(self.crossroad.grid)
        self.cell_size = 15
        self.size = self.width, self.height = self.widht_in_cell * self.cell_size + 1, self.height_in_cell * self.cell_size + 1
        self.tickspeed = 100
        self.screen = pg.display.set_mode(self.size)
        self.clock = pg.time.Clock()
        self.tick = 0
        
    def get_waiting_color(self, wait_time):
        wait_time = max(0, min(50, wait_time))
        t = wait_time / 50.0

        start_color = pg.Color(0, 200, 0)
        end_color = pg.Color(200, 0, 0)

        r = int((1 - t) * start_color.r + t * end_color.r)
        g = int((1 - t) * start_color.g + t * end_color.g)
        b = int((1 - t) * start_color.b + t * end_color.b)

        return pg.Color(r, g, b)
    
    def get_color(self, target):
        color = ''
        if isinstance(target, Cell):
            if isinstance(target, Roadside):
                color = 'gray'
            elif isinstance(target, Road):
                if isinstance(target, TrafficLight):
                    match target.light_signal:
                        case LightSignal.GREEN:
                            color = 'lime'
                        case LightSignal.YELLOW:
                            color = 'yellow'
                        case LightSignal.RED:
                            color = 'red'
                        case _:
                            color = 'lightgray'
                else:
                    color = 'lightgray'
            else:
                color = 'green'
            return pg.Color(color)
        elif isinstance(target, Car):
            return self.get_waiting_color(target.waiting_time)
        else:
            return pg.Color('green')
        
    def update(self):
        self.car_controller.update()
        self.tl_controller.update()
        
    def draw_dashed_line(self, surface, color, start_pos, end_pos, dash_length=10, space_length=5, width=1):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dx, dy = x2 - x1, y2 - y1
        distance = (dx**2 + dy**2)**0.5
        dashes = int(distance / (dash_length + space_length))

        for i in range(dashes + 1):
            start = (
                x1 + i * (dash_length + space_length) * dx / distance,
                y1 + i * (dash_length + space_length) * dy / distance,
            )
            end = (
                x1 + (i * (dash_length + space_length) + dash_length) * dx / distance,
                y1 + (i * (dash_length + space_length) + dash_length) * dy / distance,
            )
            if ((end[0] - x1)**2 + (end[1] - y1)**2)**0.5 > distance:
                end = (x2, y2)
            pg.draw.line(surface, color, start, end, width)

    def draw_road_markings(self):
        dash_length = 10
        space_length = 5
        marking_width = 1
        bold_line_width = 2

        vertical_positions = range(
            (self.road_lenght + 2) * self.cell_size, 
            self.width - (self.road_lenght + 2) * self.cell_size, 
            self.cell_size
        )
        horizontal_positions = range(
            (self.road_lenght + 2) * self.cell_size, 
            self.height - (self.road_lenght + 2) * self.cell_size, 
            self.cell_size
        )

        for x in vertical_positions:
            self.draw_dashed_line(
                self.screen, 'white', (x, 0), (x, self.road_lenght * self.cell_size),
                dash_length, space_length, marking_width
            )
            self.draw_dashed_line(
                self.screen, 'white', (x, self.height - self.road_lenght * self.cell_size), (x, self.height),
                dash_length, space_length, marking_width
            )

        for y in horizontal_positions:
            self.draw_dashed_line(
                self.screen, 'white', (0, y), (self.road_lenght * self.cell_size, y),
                dash_length, space_length, marking_width
            )
            self.draw_dashed_line(
                self.screen, 'white', (self.width - self.road_lenght * self.cell_size, y), (self.width, y),
                dash_length, space_length, marking_width
            )

        crossroad_offset = (self.road_lenght + self.crossroad_type.value + 1) * self.cell_size
        pg.draw.line(
            self.screen, 'white', (crossroad_offset, 0), (crossroad_offset, self.road_lenght * self.cell_size), bold_line_width
        )
        pg.draw.line(
            self.screen, 'white', (0, crossroad_offset), (self.road_lenght * self.cell_size, crossroad_offset), bold_line_width
        )
        pg.draw.line(
            self.screen, 'white', (crossroad_offset, self.height - self.road_lenght * self.cell_size), (crossroad_offset, self.height), bold_line_width
        )
        pg.draw.line(
            self.screen, 'white', (self.width - self.road_lenght * self.cell_size, crossroad_offset), (self.width, crossroad_offset), bold_line_width
        )
        
    def draw_text(self, text, x, y, color='black', font_size=15):
        font = pg.font.Font(None, font_size)
        text_surface = font.render(str(text), True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_screen(self):
        self.screen.fill('white')
        for x in range(0, self.widht_in_cell):
            for y in range(0, self.height_in_cell):
                if self.crossroad.grid[y][x]:
                    pg.draw.rect(self.screen, self.get_color(self.crossroad.grid[y][x]), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                    if isinstance(self.crossroad.grid[y][x], Road):
                        if self.crossroad.grid[y][x].contained_obj:
                            pg.draw.rect(self.screen, self.get_color(self.crossroad.grid[y][x].contained_obj), (x * self.cell_size + 2, y * self.cell_size + 2, self.cell_size - 2, self.cell_size - 2))
        self.draw_road_markings()
        self.draw_text(f'Cars in road - {len(self.car_controller.cars)}', 10, 10)
        self.draw_text(f'Finished cars - {self.car_controller.finish_cars}', 10, 20)
        self.draw_text(f'Total load - {round(self.tl_controller.traffic_lights_manager.total_load, 4)}', 10, 30)
        self.draw_text(f'NS load - {round(self.tl_controller.traffic_lights_manager.ns_fullness, 4)}', 10, 40)
        self.draw_text(f'EW load - {round(self.tl_controller.traffic_lights_manager.ew_fullness, 4)}', 10, 50)
        self.draw_text(f'Generations - {self.car_controller.current_generations}', 10, 60)
        self.draw_text(f'Generations delay - {round(self.car_controller.delay, 2)}', 10, 70)
        self.draw_text(f'Generations delay step - {self.car_controller.generation_delay_step}', 10, 80)
        self.draw_text(f'Generations priority - {self.car_controller.gen_priority}', 10, 90)
        self.draw_text(f'Average life time - {round(self.car_controller.avg_ltime, 2)}', 10, 100)
        self.draw_text(f'Average wait time - {round(self.car_controller.avg_wtime, 2)}', 10, 110)
        self.draw_text(f'Time - {self.tick}', 10, 120)

    def run(self):
        pg.init()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            if self.tick > 3000:
                    running = False
     
            self.draw_screen()
            self.update()
            
            self.clock.tick(self.tickspeed)
            self.tick += 1 
            pg.display.flip()
        
        pg.quit()
        self.car_controller.send_report()
        self.send_report()
 
    def send_report(self):
        GlobalData.sim_report = SimReport(self.crossroad_type, self.tl_manager_type)