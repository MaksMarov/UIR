import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import numpy as np
import os
from datetime import datetime
from itertools import groupby
from Lab3.crossroad.enums import CrossroadLightState, CrossroadType, TrafficLightControllerState


class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def _save_plot(self, plot_name):
        folder_path = os.path.join("Lab3", "crossroad", "results")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{plot_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")
        plt.savefig(file_path)
        print(f"Plot saved to {file_path}")

    def plot_congestion_over_time(self):
        ns_loads = [light.ns_load for light in self.data.traffic_light_data]
        ew_loads = [light.ew_load for light in self.data.traffic_light_data]
        loads = [light.total_load for light in self.data.traffic_light_data]
        timestamps = np.arange(len(ns_loads))
    
        if not ns_loads or not ew_loads:
            print("No congestion data available.")
            return
    
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=0.2)
    
        ns_line, = ax.plot(timestamps, ns_loads, label="NS Load", color='blue', visible=True)
        ew_line, = ax.plot(timestamps, ew_loads, label="EW Load", color='red', visible=True)
        total_line, = ax.plot(timestamps, loads, label="Total Load", color='orange', visible=True)
    
        ax.set_title("Congestion Over Time")
        ax.set_xlabel("Simulation Step")
        ax.set_ylabel("Congestion")
        ax.legend()
        ax.grid(True)
    
        check_ax = plt.axes([0.05, 0.5, 0.1, 0.15])
        check = CheckButtons(check_ax, ["NS Load", "EW Load", "Total Load"], [True, True, True])
    
        def toggle_visibility(label):
            if label == "NS Load":
                ns_line.set_visible(not ns_line.get_visible())
            elif label == "EW Load":
                ew_line.set_visible(not ew_line.get_visible())
            elif label == "Total Load":
                total_line.set_visible(not total_line.get_visible())
            fig.canvas.draw()
    
        check.on_clicked(toggle_visibility)
    
        self._save_plot("congestion_over_time")
        plt.show()
      
    def plot_reaction_time_by_load(self):
        reaction_times = [light.reaction_time for light in self.data.traffic_light_data]
        total_load = [100 * light.total_load for light in self.data.traffic_light_data]
        timestamps = np.arange(len(reaction_times))

        if not reaction_times or not total_load:
            print("No congestion data available.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, reaction_times, label="reaction_time", color='blue')
        plt.plot(timestamps, total_load, label="load %", color='red')
        plt.title("Reaction time/Total Load")
        plt.xlabel("Simulation Step")
        plt.ylabel("Value")
        plt.legend()
        plt.grid(True)
        self._save_plot("load_reaction")
        plt.show()

    def identify_peak_congestion_times(self):
        peak_loads = [light.total_load for light in self.data.traffic_light_data]

        if not peak_loads:
            print("No peak congestion data available.")
            return

        peak_time = np.argmax(peak_loads)
        max_load = peak_loads[peak_time]
        print(f"Maximum congestion ({max_load:.2f}) occurred at simulation step {peak_time}.")

    def correlation_delay_and_congestion(self):
        delays = [point.curent_delays for point in self.data.car_controller_data]
        loads = [light.total_load for light in self.data.traffic_light_data]

        if not delays or not loads:
            print("No data available for correlation analysis.")
            return

        min_length = min(len(delays), len(loads))
        correlation = np.corrcoef(delays[:min_length], loads[:min_length])[0, 1]

        print(f"Correlation between delay and load: {correlation:.2f}")

    def summary_report(self):
        report_lines = ["=== Summary Report ==="]
        if self.data.sim_report:
            report_lines.append(f"Crossroad Type: {CrossroadType(self.data.sim_report.crossroad_type).name}")
            report_lines.append(f"Traffic Light Control Type: {TrafficLightControllerState(self.data.sim_report.traffic_light_type).name}")
        else:
            report_lines.append("Simulation data is not available.")

        report_lines.append(f"Total Cars: {len(self.data.cars_data)}")

        report_lines.append(f"Average Lifetime per Car: {np.mean([car.life_time for car in self.data.cars_data]):.2f}")
        report_lines.append(f"Average Traffic Light Load: {np.mean([light.total_load for light in self.data.traffic_light_data]):.2f}")

        report_text = "\n".join(report_lines)
        print(report_text)

    def process(self):
        print("Analysis...")
        self.summary_report()
        self.identify_peak_congestion_times()
        self.correlation_delay_and_congestion()
        self.plot_congestion_over_time()
        self.plot_reaction_time_by_load()