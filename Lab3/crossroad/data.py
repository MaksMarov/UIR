import csv
from datetime import datetime
import os
from Lab3.crossroad.enums import *

class Data():
    def __init__(self):
        self.cars_data = []
        self.car_controller_data = []
        self.car_controller_report = None
        self.traffic_light_data = []
        self.sim_report = None

    def export_to_csv(self):
        folder_path = os.path.join("Lab3", "crossroad", "results")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"SimData_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(["CarData"])
            writer.writerow(["wtimes", "lifetime", "finish_time"])
            for car in self.cars_data:
                writer.writerow([car.wtimes, car.life_time, car.finish_time])

            writer.writerow(["CarControllerData"])
            writer.writerow(["cars_count", "delay"])
            for controller in self.car_controller_data:
                writer.writerow([controller.current_cars, controller.curent_delays])

            if self.car_controller_report:
                writer.writerow(["CarControllerReport"])
                writer.writerow(["start_delay", "end_delay", "generations", "finish_cars"])
                writer.writerow([
                    self.car_controller_report.start_delay,
                    self.car_controller_report.end_delay,
                    self.car_controller_report.generations,
                    self.car_controller_report.finish_cars
                ])

            writer.writerow(["TrafficLightData"])
            writer.writerow(["total_load", "ns_load", "ew_load", "current_state"])
            for light in self.traffic_light_data:
                writer.writerow([
                    light.total_load,
                    light.ns_load,
                    light.ew_load,
                    light.current_state.value
                ])

            if self.sim_report:
                writer.writerow(["SimReport"])
                writer.writerow(["crossroad_type", "traffic_light_type"])
                writer.writerow([
                    self.sim_report.crossroad_type.value,
                    self.sim_report.traffic_light_type.value
                ])

    def import_from_csv(self, file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            section = None

            for row in reader:
                if not row:
                    continue

                if row[0] in ["CarData", "CarControllerData", "CarControllerReport", "TrafficLightData", "SimReport"]:
                    section = row[0]
                    continue

                if section == "CarData" and len(row) == 3:
                    self.cars_data.append(CarDataPoint(float(row[0]), float(row[1]), float(row[2])))

                elif section == "CarControllerData" and len(row) == 2:
                    self.car_controller_data.append(CarConrollerDataPoint(int(row[0]), float(row[1])))

                elif section == "CarControllerReport" and len(row) == 4:
                    self.car_controller_report = CarControllerReport(float(row[0]), float(row[1]), int(row[2]), int(row[3]))

                elif section == "TrafficLightData" and len(row) == 4:
                    self.traffic_light_data.append(TrafficLightDataPoint(
                        float(row[0]),
                        float(row[1]),
                        float(row[2]),
                        CrossroadLightState(int(row[3]))
                    ))

                elif section == "SimReport" and len(row) == 2:
                    self.sim_report = SimReport(
                        CrossroadType(int(row[0])),
                        TrafficLightControllerState(int(row[1]))
                    )

class CarDataPoint():
    def __init__(self, wtimes, lifetime, finish_time):
        self.wtimes = wtimes
        self.life_time = lifetime
        self.finish_time = finish_time

class CarConrollerDataPoint():
    def __init__(self, cars_count, delay):
        self.current_cars = cars_count
        self.curent_delays = delay

class CarControllerReport():
    def __init__(self, start_delay, end_delay, generations, finish_cars):
        self.start_delay = start_delay
        self.end_delay = end_delay
        self.generations = generations
        self.finish_cars = finish_cars

class TrafficLightDataPoint():
    def __init__(self, total_load, ns_load, ew_load,current_delay, current_state):
        self.total_load = total_load
        self.ns_load = ns_load
        self.ew_load = ew_load
        self.reaction_time = current_delay
        self.current_state = current_state

class SimReport():
    def __init__(self, crossroad_type, tlight_type):
        self.crossroad_type = crossroad_type
        self.traffic_light_type = tlight_type

GlobalData = Data()