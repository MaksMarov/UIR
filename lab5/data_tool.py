import csv
import tkinter as tk
from tkinter import filedialog
import os
from grid import Grid
from enums import CellType


def save_simulation_results_csv(dead_count, survived_count, evacuation_time):
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Choose file to save results"
    )

    if not file_path:
        return

    write_header = not os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        if write_header:
            writer.writerow(["Dead", "Survived", "Evacuation Time"])
        
        writer.writerow([dead_count, survived_count, evacuation_time])

    print(f"Results was saved in {file_path}")
    
def load_simulation_data():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if not file_path:
        print("File wasn't selected.")
        return None, None, None, None

    dead_counts, survived_counts, evacuation_times = [], [], []

    with open(file_path, newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            dead_counts.append(int(row[0]))
            survived_counts.append(int(row[1]))
            evacuation_times.append(int(row[2]))

    return file_path, dead_counts, survived_counts, evacuation_times
    
def save_to_csv(grid):
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if filename:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for row in grid.grid:
                writer.writerow([cell.cell_type.value for cell in row])
                
    return grid
            
def import_map():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
    if filename:
        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                grid_data = [list(map(int, row)) for row in reader]

            height = len(grid_data)
            width = len(grid_data[0]) if height > 0 else 0

            grid = Grid(width, height)

            for y, row in enumerate(grid_data):
                for x, cell_value in enumerate(row):
                    grid.set_cell(x, y, CellType(cell_value))

            return grid
        except FileNotFoundError:
            print("Map file does not exist")
            return None
