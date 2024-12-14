from random import randint
from numpy import random as rnd
from Lab3.crossroad.enums import IntentionalDirection, GenerationPriority, CellDirection
from Lab3.crossroad.cell import TrafficLight, UniDirectionalRoad, MultiDirectionalRoad
from Lab3.crossroad.data import CarDataPoint, CarConrollerDataPoint, CarControllerReport, GlobalData

class Car():
    def __init__(self):
        self.intentional_direction = IntentionalDirection(rnd.choice(range(1, 5), p = [0.4, 0.4, 0.1, 0.1]))
        self.position = None
        self.next_position = None
        self.move_direction = None
        self.waiting_time = 0
        self.wtimes = []
        self.last_move_possible = True
        self.life_time = 0
        
    def update_direction(self):
        if self.position:
            self.move_direction = self.position.direction

    def update(self):
        self.next_position = self.get_next_position()  

        if self.can_move_here(self.next_position) and not self.last_move_possible:
            self.waiting_time += 1
            self.last_move_possible = True
        elif self.can_move_here(self.next_position):
            self.move_to(self.next_position)
            self.waiting_time = 0
            self.last_move_possible = True
        else:
            self.waiting_time += 1
            self.last_move_possible = False

        self.wtimes.append(self.waiting_time)
        self.life_time +=1
            
    def finish(self):
        self.position.contained_obj = None
        self.position.position = None

    def move_to(self, cell):
        self.position.contained_obj = None
        self.position = cell
        self.position.contained_obj = self
        
    def can_move_here(self, cell):
        if cell:
            return cell.get_availability()
        else:
            print(f"Error. Cell to move is not exist. cell = {cell}")
        
    def get_next_position(self):
        if isinstance(self.position, UniDirectionalRoad):
            waiting = randint(1, 3)
            match self.intentional_direction:
                case IntentionalDirection.RIGHT:
                    return self.position.right_lane if self.position.right_lane and self.waiting_time < waiting else self.position.straight_path
                case IntentionalDirection.LEFT:
                    return self.position.left_lane if self.position.left_lane and self.waiting_time < waiting else self.position.straight_path
                case IntentionalDirection.U_TURN:
                    return self.position.left_lane if self.position.left_lane and self.waiting_time < waiting else self.position.straight_path
                case IntentionalDirection.STRAIGHT:
                    if self.waiting_time < 1:
                        if self.position.left_lane and self.position.right_lane:
                            return self.position.straight_path
                        elif self.position.left_lane:
                            return self.position.left_lane
                        elif self.position.right_lane:
                            if self.position.right_lane.right_lane:
                                return self.position.right_lane
                            else:
                                return self.position.straight_path
                        else:
                            return self.position.straight_path
                    else:
                        return self.position.straight_path
        elif isinstance(self.position, MultiDirectionalRoad):
            fork = self.position.get_fork_by_direction(self.move_direction)
            waiting = randint(5, 10)
            match self.intentional_direction:
                case IntentionalDirection.RIGHT:
                    return fork.right_path if fork.right_path else fork.get_straight_or_any_path()
                case IntentionalDirection.LEFT:
                    if self.waiting_time < waiting:
                        return fork.left_path if fork.left_path else fork.get_straight_or_any_path()
                    else:
                        return fork.get_straight_or_any_path()
                case IntentionalDirection.U_TURN:
                    return fork.back_way if fork.back_way else fork.get_straight_or_any_path()
                case IntentionalDirection.STRAIGHT:
                    return fork.get_straight_or_any_path()
        else:
            print(f"Error. Current position is not a Road. Cell = {self.position}")
        

class CarController():
    def __init__(self, points, cars_per_generation, start_delay_tick, inf_generation = True, generations_count = 100, end_delay_tick = None, gen_priority = GenerationPriority.NONE):
        self.start_delay = start_delay_tick
        self.end_delay = end_delay_tick
        self.delay = self.start_delay
        self.generation_delay_step = 0 if not self.end_delay else self.calc_gen_step(generations_count)
        self.generations_count = None if inf_generation else generations_count
        self.generate_cars
        self.start_points, self.end_points = points
        self.current_time = 0
        self.current_generations = 0
        self.cars_per_generation = min(cars_per_generation, len(self.start_points))
        self.gen_priority = gen_priority
        self.cars = []
        self.finish_cars = 0
        self.avg_wtime = 0
        self.avg_ltime = 0
        
    def calc_gen_step(self, gen_count):
        step = (self.end_delay - self.start_delay) / (gen_count if gen_count and gen_count != 0 else 1)
        return step if step and step != 0 else (self.end_delay - self.start_delay)/abs(self.end_delay - self.start_delay)

    def calc_delay(self):
        return max(min(self.delay + self.generation_delay_step, max(self.start_delay, self.end_delay)), min(self.start_delay, self.end_delay))
    
    def calc_avg_wtime(self):
        wtimes = []
        for car in self.cars:
            wtimes.append(car.waiting_time)
            
        return sum(wtimes) / len(wtimes)
    
    def calc_avg_ltime(self):
        ltimes = []
        for car in self.cars:
            ltimes.append(car.life_time)
            
        return sum(ltimes) / len(ltimes)
        
    def need_to_gen_cars(self):
        if self.current_time >= self.delay:
            if self.generations_count is None:
                return True
            else:
                return self.generations_count - self.current_generations
        else:
            return False
        
    def update(self):
        for car in self.cars:
            car.update()
            if car.position in self.end_points:
                car.finish()
                self.cars.remove(car)
                GlobalData.cars_data.append(CarDataPoint(car.wtimes, car.life_time, self.current_time))
                self.finish_cars += 1
                
        if len(self.cars) > 1:
            self.avg_ltime = self.calc_avg_ltime()
            self.avg_wtime = self.calc_avg_wtime()

        if self.need_to_gen_cars():
            self.generate_cars()
            self.current_time = 0
        else:
            self.current_time += 1
            
        GlobalData.car_controller_data.append(CarConrollerDataPoint(len(self.cars), self.delay))
                
    def generate_cars(self):
        if self.gen_priority != GenerationPriority.NONE:
            ns_positions = [pos for pos in self.start_points if pos.direction in (CellDirection.NORTH, CellDirection.SOUTH)]
            ew_positions = [pos for pos in self.start_points if pos.direction in (CellDirection.EAST, CellDirection.WEST)]
            koeff = 3

            if self.gen_priority == GenerationPriority.NS:
                priority_positions = ns_positions
                non_priority_positions = ew_positions
            elif self.gen_priority == GenerationPriority.EW:
                priority_positions = ew_positions
                non_priority_positions = ns_positions

            priority_available = [pos for pos in priority_positions if pos.get_availability()]
            non_priority_available = [pos for pos in non_priority_positions if pos.get_availability()]

            priority_new_car_count = min(randint(int(self.cars_per_generation / 3 / 2), int(self.cars_per_generation / 2)), len(priority_available))
            priority_positions = rnd.choice(priority_available, size=priority_new_car_count, replace=False)
            for position in priority_positions:
                new_car = Car()
                new_car.position = position
                new_car.update_direction()
                new_car.position.contained_obj = new_car
                self.cars.append(new_car)

            non_priority_new_car_count = min(randint(int(self.cars_per_generation / (3 * koeff) / 2), int(self.cars_per_generation / koeff / 2)), len(non_priority_available))
            non_priority_positions = rnd.choice(non_priority_available, size=non_priority_new_car_count, replace=False)
            for position in non_priority_positions:
                new_car = Car()
                new_car.position = position
                new_car.update_direction()
                new_car.position.contained_obj = new_car
                self.cars.append(new_car)

            if priority_new_car_count or non_priority_new_car_count:
                self.current_generations += 1
                if self.end_delay:
                    self.delay = self.calc_delay()
        else:
            available_positions = [position for position in self.start_points if position.get_availability()]
            new_car_count = min(randint(int(self.cars_per_generation / 3), self.cars_per_generation), len(available_positions))
            positions = rnd.choice(available_positions, size=new_car_count, replace=False)
            for position in positions:
                new_car = Car()
                new_car.position = position
                new_car.update_direction()
                new_car.position.contained_obj = new_car
                self.cars.append(new_car)

            if new_car_count:
                self.current_generations += 1
                if self.end_delay:
                    self.delay = self.calc_delay()
                    
    def send_report(self):
        GlobalData.car_controller_report = CarControllerReport(self.start_delay, self.end_delay, self.current_generations, self.finish_cars)